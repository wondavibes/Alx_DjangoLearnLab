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


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["post"])
    def follow(self, request, pk=None):
        user_to_follow = self.get_object()

        if user_to_follow == request.user:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.user.following.add(user_to_follow)
        return Response({"detail": f"You are now following {user_to_follow.username}."})

    @action(detail=True, methods=["post"])
    def unfollow(self, request, pk=None):
        user_to_unfollow = self.get_object()

        if user_to_unfollow == request.user:
            return Response(
                {"detail": "You cannot unfollow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.user.following.remove(user_to_unfollow)
        return Response({"detail": f"You have unfollowed {user_to_unfollow.username}."})

class UserView(generics.GenericAPIView):
    ...