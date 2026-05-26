from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control text-light bg-dark',
            'style': 'border-color: darkorange'
        }),
        error_messages={'required': 'Username is required!'}
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control text-light bg-dark',
            'style': 'border-color: darkorange'
        }),
        error_messages={'required': 'Password is required!'}
    )
