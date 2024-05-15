from django.contrib import admin
from django.urls import path, include
from postmails import views

urlpatterns = [
    path('', views.home, name='index'),
]