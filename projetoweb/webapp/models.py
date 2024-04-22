from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
     foto = models.ImageField(
        upload_to='fotos_perfil/',
        blank=True,
        null=True,
        default='fotos_perfil/default.jpg'
    )
     
     saldo = models.FloatField(
         default=0
     )

     def __str__(self):
        return self.username