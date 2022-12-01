from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager


class User(AbstractUser):
    phone_number = models.CharField(max_length=11, unique=True, verbose_name='شماره موبایل')

    objects = UserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f'{self.username} - {self.phone_number}'


class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11, unique=True)
    code = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'کد یکبار مصرف'
        verbose_name_plural = 'کدهای یکبار مصرف'

    def __str__(self):
        return f'{self.phone_number} - {self.code}'
