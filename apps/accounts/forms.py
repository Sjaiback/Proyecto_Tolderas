from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={"placeholder": "DNI o usuario", "autocomplete": "username"}),
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"placeholder": "Tu contrasena", "autocomplete": "current-password"}),
    )


class ManagedUserForm(UserCreationForm):
    role = forms.ChoiceField(label="Rol", choices=UserProfile.Role.choices)
    dni = forms.CharField(label="DNI", required=False)
    phone = forms.CharField(label="Telefono", required=False)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "role", "dni", "phone")


class ManagedUserEditForm(forms.ModelForm):
    role = forms.ChoiceField(label="Rol", choices=UserProfile.Role.choices)
    dni = forms.CharField(label="DNI", required=False)
    phone = forms.CharField(label="Telefono", required=False)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "is_active")
