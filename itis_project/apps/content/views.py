from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .forms import PostForm

from .models import *

# TODO redirection after liking


@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    course_num_word = {'1': 'первый', '2': 'второй',
                       '3': 'третий', '4': 'четвертый'}
    posts = Post.objects.filter(author=request.user).count
    likes = Like.objects.filter(user=request.user).count
    args = {'profile': user_profile, 'post_count': posts, 'like_count': likes,
            'course': course_num_word.get(str(user_profile.course_number))}
    return render(request, 'profile_page.html', args)


@login_required
def profile_edit(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        user_profile.course_number = request.POST.get('course')
        user_profile.save()
        return redirect('profile_url')

    args = {'profile': user_profile}
    return render(request, 'profile_edit_page.html', args)


@login_required
def create_post(request):
    subjects = []
    for i in range(4):
        subjects.append(Subject.objects.filter(course_number=i + 1))

    args = {'username': request.user.username, 'subjects': subjects}

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.subject = Subject.objects.get(name=request.POST.get('subject'))
            post.save()
            return redirect('feed_url')
    else:
        form = PostForm

    args['form'] = form
    return render(request, 'create_post.html', args)


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
    args = {'post': post, 'owner': 'False', 'username': request.user.username}

    if request.user == post.author:
        args['owner'] = 'True'

    return render(request, 'post.html', args)


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