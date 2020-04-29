from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.template.context_processors import csrf
from django.urls import reverse, reverse_lazy
from django.views.generic import View
from django.contrib import auth
from django.shortcuts import redirect


class LoginInView(View):
    def get(self, request):
        args = {}
        args.update(csrf(request))
        return render(request, 'login_in_page.html', args)

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
            args['login_error'] = 'Неверный имя пользователя или пароль'
            return render(request, 'login_in_page.html', args)


def logout(request):
    auth.logout(request)
    return redirect('feed_url')


class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'register_page.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        args = {}
        if form.is_valid():
            form.save()
            return redirect('feed_url')
        else:
            args['register_error'] = form.errors
            return render(request, 'register_page.html', args)


