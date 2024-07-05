from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, reverse_lazy, include

from users import apps
from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegisterView, ProfileView, generate_new_password, verification_view, \
    ResetUserPasswordView

app_name = apps.UsersConfig.name

urlpatterns = [
    path('confirm/<str:token>/', verification_view, name='verification'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/genpassword/', generate_new_password, name='generate_new_password'),
    path('password_reset/',
         ResetUserPasswordView.as_view(template_name="users/password_reset_form.html",
                                       email_template_name="users/password_reset_email.html",
                                       success_url=reverse_lazy("users:login")),
         name='password_reset'),
    path('password_reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html',
                                          success_url=reverse_lazy("users:password_reset_complete")),
         name='password_reset_confirm'),
    path('password_reset/complete/',
         PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete')
]