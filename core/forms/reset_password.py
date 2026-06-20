# Copyright (c) 2026, Alexander Suvorov. All rights reserved.
from django import forms


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(
        error_messages={'required': 'New Password is required!'},
        required=True
    )
    confirm_password = forms.CharField(
        error_messages={'required': 'Confirm Password is required!'},
        required=True
    )
