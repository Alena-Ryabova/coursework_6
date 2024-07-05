import secrets
import string
import random

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView as BaseLoginView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.views import LogoutView as BaseLogoutView


# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from users.models import User
from users.forms import UserRegisterForm, UserProfileForm, ChangeUserPasswordForm


class LoginView(BaseLoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('postmails:mailing_list')


class LogoutView(BaseLogoutView):
    success_url = reverse_lazy('postmails:mailing_list')


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = ''.join([str(random.randint(0, 9)) for _ in range(12)])
        user.token = token

        user.save()
        current_site = self.request.get_host()
        verification_link = f'http://{current_site}/users/confirm/{token}/'
        message = f'Поздравляем с регистрацией! \nДля верификации перейдите по ссылке \n{verification_link}'
        send_mail(
            subject='Регистрация',
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False
        )
        print(message)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('postmails:mailing_list')


def verification_view(request, token):
    user = User.objects.filter(token=token).first()
    if user:
        user.is_active = True
        user.save()

    return redirect(reverse('users:login'))


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')
    login_url = reverse_lazy('users:login')
    redirect_field_name = "redirect_to"

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):
    new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    send_mail(
        subject='Вы сменили пароль',
        message=f'Ваш новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_password)
    request.user.save()

    return redirect(reverse('users:login'))


class ResetUserPasswordView(PasswordResetView):
    form_class = ChangeUserPasswordForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        if self.request.method == 'POST':
            email = self.request.POST['email']
            try:
                user = User.objects.get(email=email)
                alphabet = string.ascii_letters + string.digits
                password = "".join(secrets.choice(alphabet) for i in range(10))
                user.set_password(password)
                user.save()
                message = f"Ваш новый пароль:\n{password}"
                send_mail(
                    "Смена пароля",
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            except User.DoesNotExist:
                return render(self.request, 'users/password_reset_form.html',
                              {'error_message': 'Пользователь с таким email не найден'})
        return super().form_valid(form)


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    pass
