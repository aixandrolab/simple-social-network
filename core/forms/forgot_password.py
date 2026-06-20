# Copyright (c) 2026, Alexander Suvorov. All rights reserved.
from django import forms


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        max_length=255,
        error_messages={'required': 'Password is required!'},
        required=True,
    )
