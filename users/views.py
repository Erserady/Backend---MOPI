from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .serializers import UserCreateSerializer, UserSerializer, LoginSerializer
from django.db import transaction


User = get_user_model()

class RegisterView(GenericAPIView):
    """
    Registro de usuarios:
    - acepta JSON con 'username', 'email' y 'password'
    - crea el usuario (User.objects.create_user)
    - genera/recupera token y devuelve token + datos del usuario
    """
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        # get_serializer ya pasa context={'request': request}
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # El serializer.create() debe devolver el objeto user ya guardado
        user = serializer.save()

        # crear o recuperar token de DRF
        token, _ = Token.objects.get_or_create(user=user)

        # serializar respuesta del usuario (sin password)
        user_data = UserSerializer(user).data

        return Response(
            {"token": token.key, "user": user_data},
            status=status.HTTP_201_CREATED
        )


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)