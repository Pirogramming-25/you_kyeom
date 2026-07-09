
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_image', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': '소개글을 입력하세요...'
            }),
        }