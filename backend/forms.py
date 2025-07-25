# forms.py

from django import forms
from .models import CustomUser  # или User, если ты его так назвала

class AvatarUploadForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['avatar']  # только поле аватара
