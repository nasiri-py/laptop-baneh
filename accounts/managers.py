from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number, username, password):
        if not phone_number:
            raise ValueError('user must have phone number')
        if not username:
            raise ValueError('user must have username')
        user = self.model(phone_number=phone_number, username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, username, password):
        user = self.create_user(phone_number, username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

