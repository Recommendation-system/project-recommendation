from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'theme', 'title', 'content']

        widgets = {
            'author': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'name': 'title'}),
            'theme': forms.Select(attrs={'class': 'form-control', 'name': 'theme'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'name': 'text'}),
        }




