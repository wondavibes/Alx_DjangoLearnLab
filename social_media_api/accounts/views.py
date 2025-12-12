from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer


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
