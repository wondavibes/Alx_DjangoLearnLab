from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from .models import CustomUser
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    UserFollowSerializer,
)


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)

        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": token,
                "message": "User registered successfully.",
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]  # type: ignore
        token = serializer.validated_data["token"]  # type: ignore

        return Response(
            {"token": token, "user": UserSerializer(user).data},
            status=status.HTTP_200_OK,
        )


class UserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


from django.shortcuts import get_object_or_404
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType


class FollowUserView(generics.GenericAPIView):
    """Follow another user. Expects `user_id` path kwarg."""

    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(CustomUser, pk=user_id)

        if target == request.user:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # static checkers may not know request.user is CustomUser, but runtime will work
        request.user.following.add(target)

        # create a notification for the user being followed
        if target != request.user:
            Notification.objects.create(
                recipient=target,
                actor=request.user,
                verb="started following you",
                target=request.user,
                target_content_type=ContentType.objects.get_for_model(
                    request.user.__class__
                ),
                target_object_id=request.user.id,
            )

        return Response(
            {"detail": f"You are now following {target.username}."},
            status=status.HTTP_200_OK,
        )


class UnfollowUserView(generics.GenericAPIView):
    """Unfollow another user. Expects `user_id` path kwarg."""

    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(CustomUser, pk=user_id)

        if target == request.user:
            return Response(
                {"detail": "You cannot unfollow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.user.following.remove(target)
        return Response(
            {"detail": f"You have unfollowed {target.username}."},
            status=status.HTTP_200_OK,
        )
