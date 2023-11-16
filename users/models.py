from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Email')

    phone_number = models.CharField(max_length=35, verbose_name='Телефонный номер', **NULLABLE)
    confirmation_token = models.CharField(max_length=200, verbose_name='Токен подтверждения', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []