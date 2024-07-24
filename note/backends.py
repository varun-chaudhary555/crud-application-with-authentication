from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            if not user.is_active:
                request.session['deactivated_account'] = True
                return None
        except User.DoesNotExist:
            return None
        
        return super().authenticate(request, username=username, password=password, **kwargs)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            if not user.is_active:
                request.session['deactivated_account'] = True
                print(f"User {username} is deactivated.")
                return None
        except User.DoesNotExist:
            return None

        return super().authenticate(request, username=username, password=password, **kwargs)

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
