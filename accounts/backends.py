from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailBackend(ModelBackend):
    # pylint: disable=W0237
    def authenticate(self, request, email=None, password=None, **kwargs):
        user_auth = get_user_model()
        try:
            user = user_auth.objects.get(email=email)
            if user.check_password(password):
                return user
            return None
        except user_auth.DoesNotExist:
            return None

    # pylint: disable=R1710
    def get_user(self, user_id):
        user_auth = get_user_model()
        try:
            return user_auth.objects.get(pk=user_id)
        except user_auth.DoesNotExist:
            return None
