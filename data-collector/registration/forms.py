from django import forms
from django.contrib.auth.forms import UserCreationForm
from user.models import CustomUser


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "password1", "password2"]
