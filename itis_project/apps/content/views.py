from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .forms import PostForm

from .models import *
from .logic import get_recommendations, create_recommendations


@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    course_num_word = {'1': 'первый', '2': 'второй',
                       '3': 'третий', '4': 'четвертый'}
    posts = Post.objects.filter(author=request.user).count
    likes = Like.objects.filter(user=request.user).count
    context = {'profile': user_profile, 'post_count': posts, 'like_count': likes,
               'course': course_num_word.get(str(user_profile.course_number))}
    return render(request, 'profile_page.html', context=context)


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
def feed_list(request):
    subjects = Subject.objects.filter(course_number=UserProfile.objects.get(user=request.user).course_number)

    subject_name = request.GET.get('subject', 'recommend')

    if subject_name == 'recommend':
        subj = 'recommend'
        posts = list(Post.objects.filter(subject__course_number=UserProfile.objects.get(
            user=request.user).course_number).order_by('-likes'))[:15]
        create_recommendations(UserProfile.objects.get(user__username=request.user.username).user, 30)

        print(get_recommendations())
        posts.sort(key=recommend, reverse=True)
    else:
        subj = subjects[0]
        try:
            subj = Subject.objects.get(name=subject_name)
        except Exception:
            pass
        posts = Post.objects.filter(subject=subj)

    paginator = Paginator(posts, 3)

    page_number = request.GET.get('page', 1)
    post_list = paginator.get_page(page_number)

    previous_url = next_url = '?page={}'.format(post_list.number)
    if post_list.has_previous():
        previous_url = '?page={}'.format(post_list.previous_page_number())
    if post_list.has_next():
        next_url = '?page={}'.format(post_list.next_page_number())

    username = request.user.username
    context = {
        'subject_selected': subj,
        'username': username,
        'subjects': subjects,
        'paginator_object': post_list,
        'next_url': next_url,
        'previous_url': previous_url
    }

    return render(request, 'lenta.html', context=context)


@login_required
def create_post(request):
    context = {'username': request.user.username, 'subjects': get_subjects_dir()}

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

    context['form'] = form
    return render(request, 'create_post.html', context=context)


@login_required
def post_details(request, post_slug):
    post = get_object_or_404(Post, slug__iexact=post_slug)
    context = {'post': post, 'owner': 'False', 'username': request.user.username}

    if request.user == post.author:
        context['owner'] = 'True'

    return render(request, 'post.html', context=context)


@login_required
def post_edit(request, post_slug):
    post = get_object_or_404(Post, slug__iexact=post_slug)
    if request.user == post.author:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.subject = Subject.objects.get(name=request.POST.get('subject'))
                post.save()
                return redirect('/content/post/{}/'.format(post_slug))
        else:
            form = PostForm(instance=post)
            context = {'subjects': get_subjects_dir(), 'username': request.user.username,
                       'form': form, 'post': post}
            return render(request, 'edit_post.html', context=context)
    else:
        raise Http404


@login_required
def like_post(request):
    post_obj = None
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
    return redirect('/content/post/{}/'.format(post_obj.slug))


def recommend(post):
    return get_recommendations().get(post.subject, 0)


def get_subjects_dir():
    subjects = dir()
    for i in range(1, 5):
        subjects.append(Subject.objects.filter(course_number=i))

    return subjects
