from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, PasswordInput
from apps.models import User, NewsReceiver


class RegisterForm(ModelForm):
    confirm_password = CharField(max_length=255, widget=PasswordInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'confirm_password')

    def clean_password(self):
        password = self.data.get('password')
        confirm_password = self.data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError('Confirm password is incorrect!')
        return make_password(password)

    def clean_email(self):
        email = self.data.get('email')
        users_with_emails = User.objects.exclude(email__isnull=True).exclude(email='')
        emails = list(users_with_emails.values_list('email', flat=True))
        if email in emails:
            raise ValidationError('This email belongs to another user')
        return email


class EmailForm(ModelForm):
    class Meta:
        model = NewsReceiver
        fields = ('email',)

    def clean_email(self):
        email = self.data.get('email')
        if NewsReceiver.objects.filter(email=email):
            raise ValidationError('This email has already been registered!')
        return email


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ('image', 'first_name', 'last_name', 'username', 'email')
