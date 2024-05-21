from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views import View

from authapp.forms import LoginForm, RegisterForm


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'authapp/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('home'))  # Перенаправление на главную страницу после успешного входа
            else:
                error_message = "Неверные учетные данные"
                return render(request, 'authapp/login.html', {'form': form, 'error_message': error_message})
        else:
            error_message = "Недействительная форма"
            return render(request, 'authapp/login.html', {'form': form, 'error_message': error_message})


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'authapp/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
        return render(request, './authapp/register.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')  # Перенаправление на главную страницу после выхода
