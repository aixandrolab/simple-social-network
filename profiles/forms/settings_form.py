from django import forms

from profiles.models.profile_model import Profile


class SettingsForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=40)

    class Meta:
        model = Profile
        fields = ['email', 'biography', 'gender', 'age']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user_id:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, commit=True):
        profile = super().save(commit=False)

        if self.instance and self.instance.user_id:
            user = self.instance.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']

            if commit:
                user.save()

        if commit:
            profile.save()

        return profile
