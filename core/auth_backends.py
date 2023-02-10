from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend, UserModel


class MyModelBackend(BaseBackend):

    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        if phone_number is None or password is None:
            return
        try:
            user = get_user_model().objects.get(phone_number=phone_number)
        except UserModel.DoesNotExist:
            return
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def user_can_authenticate(self, user):
        is_active = getattr(user, "is_active", None)
        return is_active or is_active is None
