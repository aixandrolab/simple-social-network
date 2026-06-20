# Copyright (c) 2026, Alexander Suvorov. All rights reserved.
from django import forms

from chats.models import Chat


class ChatSettingsForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['name']
        labels = {
            'name': 'Chat Name',
        }
