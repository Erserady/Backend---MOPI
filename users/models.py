from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    usuario = models.CharField(max_length=100, unique=True)   # alias o nombre de usuario
    remember_me = models.BooleanField(default=False)

    def __str__(self):
        return self.username