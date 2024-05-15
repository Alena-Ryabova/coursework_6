from django.contrib import admin
from django.urls import path, include
from postmails import views


app_name = 'users'


urlpatterns = [
    path('', views.home, name='index'),
]