from django import forms
from .models import Post, UserProfile


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['theme', 'title', 'content']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'name': 'title'}),
            'theme': forms.Select(attrs={'class': 'form-control', 'name': 'theme'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'name': 'text'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']
