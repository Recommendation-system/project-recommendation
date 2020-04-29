from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import View
from django.shortcuts import get_object_or_404
from .forms import PostForm

from .models import *


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('feed_url')
        return render(request, 'create_post.html', {'form': form})
    else:
        form = PostForm
        return render(request, 'create_post.html', {'form': form})


def feed_list(request):
    posts = Post.objects.all()
    user = request.user
    context = {
        'posts': posts,
        'user': user,
    }
    return render(request, 'index.html', context)


@login_required
def post_details(request, post_slug):
    post = get_object_or_404(Post, slug__iexact=post_slug)
    return render(request, 'post.html', context={'post': post})


@login_required
def like_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)

        if user not in post_obj.likes.all():
            post_obj.likes.add(user)
        else:
            post_obj.likes.remove(user)

        like, created = Like.objects.get_or_create(user=user, post_id=post_id)
        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        like.save()
    return redirect('feed_url')