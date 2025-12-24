from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
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


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, user_id):
    try:
        target = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    if target == request.user:
        return Response(
            {"detail": "You cannot follow yourself."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    request.user.following.add(target)
    return Response(
        {"detail": f"You are now following {target.username}."},
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request, user_id):
    try:
        target = CustomUser.objects.get(pk=user_id)
    except CustomUser.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    if target == request.user:
        return Response(
            {"detail": "You cannot unfollow yourself."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    request.user.following.remove(target)
    return Response(
        {"detail": f"You have unfollowed {target.username}."}, status=status.HTTP_200_OK
    )
