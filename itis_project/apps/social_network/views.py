from django.shortcuts import render

from .models import Post


def feed(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {'posts': posts})


def login(request):
    return render(request, 'login/login_in_page.html')


def register(request):
    return render(request, 'login/register_page.html')
