from django.conf import settings
from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    """
    Модель для хранения информации о клиентах
    """
    email = models.CharField(unique=True, verbose_name='Почта')
    name = models.CharField(max_length=100, verbose_name='Ф.И.О.')
    comment = models.CharField(max_length=200, verbose_name='Комментарий', **NULLABLE)
    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return f'{self.name} - {self.email} '

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Mailing(models.Model):
    """
    Модель для хранения информации о рассылках
    """
    name = models.CharField(max_length=50, verbose_name='Название рассылки')
    sent_date = models.DateField(auto_now_add=True, verbose_name='Дата')
    sent_time = models.TimeField(auto_now_add=True, verbose_name='Время')
    periodicity = models.CharField(max_length=50, verbose_name='Периодичность')
    status = models.CharField(max_length=50, verbose_name='Статус')
    is_active = models.BooleanField(default=True, verbose_name="Действующая")
    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Log(models.Model):
    """
    Модель для хранения информации о логах рассылок
    """

    time = models.DateTimeField(
        verbose_name="Дата и время попытки отправки", auto_now_add=True
    )
    status = models.BooleanField(verbose_name="Статус попытки отправки")
    server_response = models.CharField(
        max_length=150, verbose_name="Ответ сервера почтового сервиса", **NULLABLE
    )
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name="Рассылка")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Клиент")

    def __str__(self):
        return f"{self.client} {self.mailing} {self.time} {self.status} {self.server_response}"

    class Meta:
        verbose_name = "Лог рассылки"
        verbose_name_plural = "Логи рассылок"


class Message(models.Model):
    """
    Модель для хранения информации о сообщении для рассылки
    """

    title = models.CharField(max_length=255, verbose_name="Тема")
    message = models.TextField(verbose_name="Сообщение")
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')
    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
