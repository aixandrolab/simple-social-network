# Copyright (c) 2026, Alexander Suvorov. All rights reserved.
from django import forms


class Enable2FAForm(forms.Form):
    verification_code = forms.CharField(
        max_length=6,
        min_length=6,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'field',
            'placeholder': 'Enter 6-digit code',
            'autocomplete': 'off'
        }),
        label='Verification Code'
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_verification_code(self):
        code = self.cleaned_data.get('verification_code')
        totp = self.user.profile.get_totp_device()

        if not totp or not totp.verify(code, valid_window=1):
            raise forms.ValidationError('Invalid verification code. Please try again.')

        return code
