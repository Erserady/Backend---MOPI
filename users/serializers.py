from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.db import transaction

User = get_user_model()



class UserSerializer(serializers.ModelSerializer):
    """Serializer para respuestas (no expone password)."""
    class Meta:
        model = User
        fields = ("id", "username", "email")
        read_only_fields = ("id",)


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para creación de usuarios.
    Solo acepta los campos en inglés: 'username', 'email', 'password'.
    """
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        read_only_fields = ("id",)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")

        if not username:
            raise serializers.ValidationError({"username": "El campo 'username' es obligatorio."})

        if not password:
            raise serializers.ValidationError({"password": "El campo 'password' es obligatorio."})

        # validar email
        try:
            validate_email(email)
        except Exception:
            raise serializers.ValidationError({"email": "Email inválido."})

        # validar password con validators de Django
        try:
            validate_password(password)
        except Exception as e:
            msgs = getattr(e, "messages", None)
            raise serializers.ValidationError({"password": msgs if msgs else str(e)})

        # unicidad username/email
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"username": "Ya existe un usuario con ese username."})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "Ya existe un usuario con ese email."})

        return data

    @transaction.atomic
    def create(self, validated_data):
        username = validated_data.get("username")
        email = validated_data.get("email")
        password = validated_data.get("password")

        # Preparar kwargs extras si el modelo User tiene un campo 'usuario'
        extra = {}
        user_field_names = [f.name for f in User._meta.get_fields()]
        if "usuario" in user_field_names:
            extra["usuario"] = username

        # create_user recibirá 'usuario' si corresponde al modelo
        user = User.objects.create_user(username=username, email=email, password=password, **extra)
        return user


class LoginSerializer(serializers.Serializer):
    """
    Acepta solo 'username' y 'password' (inglés).
    """
    username = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            raise serializers.ValidationError("Se requieren 'username' y 'password'.")

        request = self.context.get("request")
        user = authenticate(request=request, username=username, password=password)
        if not user:
            raise serializers.ValidationError("Credenciales incorrectas.")

        return {"user": user}