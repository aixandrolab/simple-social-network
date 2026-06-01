from django import forms


class TwoFactorLoginForm(forms.Form):
    code = forms.CharField(
        max_length=8,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'field',
            'placeholder': 'Enter 6-digit code or backup code',
            'autocomplete': 'off'
        }),
        label='Two-factor authentication code'
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_code(self):
        code = self.cleaned_data.get('code')

        if self.user.profile.verify_totp(code):
            return code

        if self.user.profile.verify_backup_code(code):
            return code

        raise forms.ValidationError('Invalid authentication code. Please try again.')
