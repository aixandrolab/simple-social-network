# Copyright (c) 2026, Alexander Suvorov. All rights reserved.
from django import forms
from django.contrib.auth import authenticate


class Disable2FAForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'field',
            'placeholder': 'Enter your password'
        }),
        label='Password'
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        user = authenticate(
            request=None,
            username=self.user.username,
            password=password
        )

        if not user:
            raise forms.ValidationError('Password is incorrect. Please try again.')

        return password
