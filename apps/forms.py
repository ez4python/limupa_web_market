from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, PasswordInput
from apps.models import User


class RegisterForm(ModelForm):
    confirm_password = CharField(max_length=255, widget=PasswordInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'confirm_password')

    def clean_password(self):
        password = self.data.get('password')
        confirm_password = self.data.get('confirm_password')
        if password != confirm_password:
            messages
            # raise ValidationError('Confirm password is incorrect!')
        return make_password(password)

    def clean_email(self):
        email = self.data.get('email')
