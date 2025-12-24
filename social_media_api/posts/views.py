# posts/views.py
from rest_framework import viewsets, permissions
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly
from .pagination import PostPagination
from rest_framework.response import Response
from notifications.models import Notification
from accounts.models import CustomUser
from django.contrib.contenttypes.models import ContentType


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    pagination_class = PostPagination
    search_fields = ["title", "content"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by("-created_at")
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)

        # notify post author about new comment
        post_author = comment.post.author
        if post_author != self.request.user:
            Notification.objects.create(
                recipient=post_author,
                actor=self.request.user,
                verb="commented on your post",
                target=comment.post,
            )


from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import NotAuthenticated
from notifications.models import Notification
from django.db import transaction
from django.db.models.query import QuerySet
from typing import cast


class FeedView(generics.ListAPIView):
    """Return posts from users the authenticated user is following,
    ordered by most recent first, paginated."""

    authentication_classes = [
        JWTAuthentication,
        TokenAuthentication,
        SessionAuthentication,
    ]
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    pagination_class = PostPagination

    def get_queryset(self) -> QuerySet[Post]:
        user = self.request.user
        if not getattr(user, "is_authenticated", False):
            raise NotAuthenticated()

        # Ensure static checkers know this is the project's CustomUser
        if not isinstance(user, CustomUser):
            raise NotAuthenticated()

        user = cast(CustomUser, user)
        following_users = user.following.all()
        return Post.objects.filter(author__in=following_users).order_by("-created_at")


class LikePostView(generics.GenericAPIView):
    authentication_classes = [
        JWTAuthentication,
        TokenAuthentication,
        SessionAuthentication,
    ]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user

        # Use atomic get_or_create to avoid race conditions where two requests
        # could create duplicate Like rows simultaneously.
        with transaction.atomic():
            like, created = Like.objects.get_or_create(post=post, user=user)
            if not created:
                return Response(
                    {"detail": "You have already liked this post."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # create a notification only when a new like was created
            if post.author != user:
                Notification.objects.create(
                    recipient=post.author,
                    actor=user,
                    verb="liked your post",
                    target=post,
                    target_content_type=ContentType.objects.get_for_model(post),
                    target_object_id=post.pk,
                )

        return Response(
            {"detail": "Post liked successfully."}, status=status.HTTP_201_CREATED
        )


class UnlikePostView(generics.GenericAPIView):
    authentication_classes = [
        JWTAuthentication,
        TokenAuthentication,
        SessionAuthentication,
    ]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        deleted_count, _ = Like.objects.filter(post=post, user=user).delete()
        if deleted_count == 0:
            return Response(
                {"detail": "You have not liked this post."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"detail": "Post unliked successfully."}, status=status.HTTP_200_OK
        )
