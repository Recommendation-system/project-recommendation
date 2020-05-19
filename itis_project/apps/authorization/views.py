from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.template.context_processors import csrf
from django.contrib.auth.models import User
from django.views.generic import View
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib import auth

from itis_project.apps.content.models import UserProfile


def home(request):
    if request.user.is_anonymous:
        return render(request, 'home_page.html')
    return redirect('feed_url')


def vk_auth_check(request):
    if request.user.is_authenticated:
        try:
            UserProfile.objects.get(user=request.user)
        except ObjectDoesNotExist:
            profile = UserProfile()
            profile.user = request.user
            profile.save()
            return redirect('home_url')
    return redirect('feed_url')


class LoginView(View):
    def get(self, request):
        args = {}
        args.update(csrf(request))
        args['info'] = 'Пожалуйста, введите Никнейм и пароль'
        return render(request, 'login_page.html', args)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        args = {}
        args.update(csrf(request))
        if user is not None:
            auth.login(request, user)
            return redirect('feed_url')
        else:
            args['info'] = 'Неверное имя пользователя или пароль'
            return render(request, 'login_page.html', args)


def logout(request):
    auth.logout(request)
    return redirect('feed_url')


class RegistrationView(View):
    def get(self, request):
        if request.user.is_anonymous:
            form = UserCreationForm()
            info = 'Пожалуйста зарегистрируйтесь чтобы продолжить'
            return render(request, 'registration_page.html', {'form': form, 'info': info})
        return redirect('feed_url')

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            profile = UserProfile()
            profile.user = auth.models.User.objects.get(username=form.cleaned_data.get('username'))
            profile.course_number = request.POST.get('course')
            profile.save()
            user = auth.authenticate(request=request,
                                     username=form.cleaned_data.get('username'),
                                     password=form.cleaned_data.get('password1'))
            auth.login(request, user=user)
            return redirect('feed_url')
        else:
            keys = list(form.errors.keys())
            if keys[0] == 'username':
                info = 'Пользователь с таким именем уже существует'
            else:
                info = 'Пароль слишком простой, либо пароли не совпадают'

            return render(request, 'registration_page.html', {'info': info})
