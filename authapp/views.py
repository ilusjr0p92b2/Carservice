from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView, FormView

from authapp.forms import LoginForm, RegisterForm, EditProfileForm, CarForm, CustomPasswordChangeForm
from authapp.models import User
from service.models import Order, Car


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


@method_decorator(login_required, name='dispatch')
class UserView(DetailView):
    model = User
    template_name = 'authapp/user_profile.html'
    context_object_name = 'user'
    user_form_class = EditProfileForm
    password_form_class = CustomPasswordChangeForm
    car_form_class = CarForm

    def get_object(self, queryset=None):
        return User.objects.get(id=self.kwargs['user_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = self.user_form_class(instance=self.request.user)
        context['password_form'] = self.password_form_class(user=self.request.user)
        context['car_form'] = self.car_form_class(instance=Car.objects.filter(owner=self.request.user).first())
        context['orders'] = Order.objects.filter(user=self.request.user)
        return context


class EditProfileView(View):
    template_name = 'authapp/user_profile.html'
    user_form_class = EditProfileForm
    password_form_class = CustomPasswordChangeForm
    car_form_class = CarForm

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_id = self.request.user.id
        user_form = self.user_form_class(request.POST, instance=request.user)
        password_form = self.password_form_class(user=request.user, data=request.POST)
        car = Car.objects.filter(owner=request.user).first()
        car_form = self.car_form_class(request.POST, instance=car)

        if 'save_user' in request.POST and user_form.is_valid():
            user_form.save()
            return redirect('user', user_id=user_id)

        if 'save_password' in request.POST and password_form.is_valid():
            password_form.save()
            return redirect('home')

        if 'save_car' in request.POST and car_form.is_valid():
            car_form.save()
            return redirect('user', user_id=user_id)

        context = self.get_context_data(
            user_form=user_form,
            password_form=password_form,
            car_form=car_form
        )
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = kwargs
        if 'user_form' not in context:
            context['user_form'] = self.user_form_class(instance=self.request.user)
        if 'password_form' not in context:
            context['password_form'] = self.password_form_class(user=self.request.user)
        if 'car_form' not in context:
            car = Car.objects.filter(owner=self.request.user).first()
            context['car_form'] = self.car_form_class(instance=car)
        return context


