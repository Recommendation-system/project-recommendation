from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from .models import Post


def index(request):
    posts = Post.objects.all()
    return render(request, 'social_network/index.html', {'posts': posts})
