from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.CharField(max_length=11, unique=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f'{self.username} - {self.phone_number}'
