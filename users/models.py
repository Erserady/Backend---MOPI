from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        COCINA = "COCINA", "Cocina"
        MESERO = "MESERO", "Mesero"
        CAJA = "CAJA", "Caja"
        ADMIN = "ADMIN", "Administrador"

    usuario = models.CharField(max_length=100, unique=True)  # alias o nombre de usuario
    remember_me = models.BooleanField(default=False)
    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.MESERO,
    )

    def __str__(self) -> str:
        return self.username
