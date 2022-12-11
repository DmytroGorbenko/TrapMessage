from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm


class LoginForm(forms.Form):
    username = forms.CharField(label="Ім'я користувача")
    password = forms.CharField(widget=forms.PasswordInput(), label="Пароль")


GROUP_CHOICE = [
    ('Користувач', 'Користувач'),
    ('Модератор', 'Модератор'),
]


class CustomUserCreationForm(UserCreationForm):
    group = forms.ChoiceField(choices=GROUP_CHOICE, label='Статус')

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email", "first_name", "last_name")


class EditUserForm(ModelForm):
    group = forms.ChoiceField(choices=GROUP_CHOICE, label='Статус')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class EditAdminForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
