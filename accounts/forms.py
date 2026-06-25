from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re


class RegisterForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]

    def clean_email(self):
        email = self.cleaned_data.get("email")

        email_pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

        if not re.match(email_pattern, email):
            raise forms.ValidationError(
                "Enter a valid email address."
            )

        return email

    def clean_password1(self):
        password = self.cleaned_data.get("password1")

        if len(password) < 6:
            raise forms.ValidationError(
                "Password must contain at least 6 characters."
            )

        if not re.search(r'\d', password):
            raise forms.ValidationError(
                "Password must contain at least one number."
            )

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise forms.ValidationError(
                "Password must contain at least one special symbol."
            )

        return password

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2:
            if password1 != password2:
                self.add_error(
                    'password2',
                    'Passwords do not match.'
                )

        return cleaned_data