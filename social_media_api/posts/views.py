# posts/views.py
from rest_framework import viewsets, permissions
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly
from .pagination import PostPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from notifications.models import Notification
from accounts.models import CustomUser


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    pagination_class = PostPagination
    search_fields = ["title", "content"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=["get"], url_path="feed")
    def feed(self, request):
        user = request.user
        # Get posts from users the current user is following
        following_users = user.following.all()

        # filter posts by following users and order by created_at descending
        feed_posts = Post.objects.filter(author__in=following_users).order_by(
            "-created_at"
        )
        # Paginate the results
        page = self.paginate_queryset(feed_posts)
        if page is not None:
            serializer = PostSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PostSerializer(feed_posts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        # prevent duplicate likes
        if Like.objects.filter(post=post, user=user).exists():
            return Response(
                {"detail": "You have already liked this post."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # create the like
        Like.objects.create(post=post, user=user)
        # create a notification
        if post.author != user:
            Notification.objects.create(
                recipient=post.author,
                actor=user,
                verb="liked your post",
                target=post,
                target_content_type=ContentType.objects.get_for_model(post),
                target_object_id=post.id,
            )
        return Response(
            {"detail": "Post liked successfully."}, status=status.HTTP_201_CREATED
        )

    def unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user

        like = Like.objects.filter(post=post, user=user).first()
        if not like:
            return Response(
                {"detail": "You have not liked this post."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        like.delete()
        return Response(
            {"detail": "Post unliked successfully."}, status=status.HTTP_200_OK
        )


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
                recipient = post_author,
                actor = self.request.user,
                verb = "commented on your post",
                target = comment.post,
                target_content_type = ContentType.objects.get_for_model(comment.post.__class__),
                target_id = comment.post.id,
                )
