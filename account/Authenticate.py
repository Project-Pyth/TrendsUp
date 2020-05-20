# Custom Email Authentication Backend

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
            success = user.check_password(password)
            if success:
                if user.check_password(password):
                    return user
        except:
            pass
        return None

    def get_user(self, uid):
        try:
            return User.objects.get(pk=uid)
        except:
            return None
