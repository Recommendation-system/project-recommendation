from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import User
from django import forms


class AuthUserForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')