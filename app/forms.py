from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UsernameField,
    PasswordChangeForm
)
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Confirm Password (again)',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {'email': 'Email'}
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email address must be unique.")
        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'class': 'form-control',
            'placeholder': 'Username',
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        })
    )


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old Password"),
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'autofocus': True,
            'class': 'form-control'
        })
    )
    new_password1 = forms.CharField(
        label=_("New Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control'
        })
    )
    new_password2 = forms.CharField(
        label=_("Confirm New Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'form-control'
        })
    )
