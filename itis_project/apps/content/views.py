from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .forms import PostForm, ProfileForm

from .models import *


@login_required
def profile_edit(request):
    profile = UserProfile.objects.get(user=request.user)
    form = ProfileForm(instance=profile)
    args = {'avatar': profile.avatar, 'form': form}
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, files=request.FILES, instance=profile)
        if form.is_valid():
            image = form.save(commit=False)
            file_size = image.avatar.size
            limit_kb = 128
            if file_size < limit_kb * 1024:
                image.save()
            else:
                args['size'] = 'Size limit: %s kb' % limit_kb
        args['errors'] = form.errors
        return render(request, 'profile_edit.html', args)
    else:
        return render(request, 'profile_edit.html', args)


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('feed_url')
        return render(request, 'create_post.html', {'form': form})
    else:
        form = PostForm
        return render(request, 'create_post.html', {'form': form})


@login_required
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
    owner = 'False'
    if request.user == post.author:
        owner = 'True'
    return render(request, 'post.html', context={'post': post, 'owner': owner})


@login_required
def post_edit(request, post_slug):
    post = Post.objects.get(slug__iexact=post_slug)
    if request.user == post.author:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save()
                post.save()
                return redirect('feed_url')
        else:
            form = PostForm(instance=post)
            return render(request, 'edit_post.html', context={'form': form, 'post': post})
    else:
        return redirect('feed_url')


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