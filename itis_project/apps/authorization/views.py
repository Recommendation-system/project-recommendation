from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render
from django.template.context_processors import csrf
from django.urls import reverse
from django.utils.text import slugify
from django.views.generic import View
from django.contrib import auth
from django.shortcuts import redirect


# TODO Пользователь не может попасть на страницу авторизации если он уже авторизован, с вк сделать что то
# TODO Длинна имени пользователя

from itis_project.apps.content.models import UserProfile


def home(request):

    return render(request, 'home_page.html')


class LoginView(View):
    def get(self, request):
        args = {}
        args.update(csrf(request))
        return render(request, 'login_page.html', args)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        args = {}
        args.update(csrf(request))
        if user is not None:
            auth.login(request, user)
            return redirect(reverse('feed_url'))
        else:
            args['error'] = 'Неверное имя пользователя или пароль'
            return render(request, 'login_page.html', args)


def logout(request):
    auth.logout(request)
    return redirect('feed_url')


class RegistrationView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'registration_page.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            profile = UserProfile()
            profile.user = auth.models.User.objects.get(username=form.cleaned_data.get('username'))
            profile.save()
            return redirect('login_url')
        else:
            keys = list(form.errors.keys())
            if keys[0] == 'username':
                error = 'Пользователь с таким именем уже существует'
            else:
                error = 'Пароль слишком простой, либо пароли не совпадают'

            return render(request, 'registration_page.html', {'error': error})
