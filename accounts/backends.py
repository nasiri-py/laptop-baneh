from .models import User


class PhoneNumberBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(phone_number=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None
