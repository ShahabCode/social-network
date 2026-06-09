from django.contrib.auth.backends import ModelBackend

from social.models import User

class PhoneAuthBackend:
    def authenticate(self, request, username=None, password=None, **kwargs):
        # username = phone
        try:
            user = User.objects.get(phone=username)
            if user.check_password(password):
                return user
            else:
                return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None