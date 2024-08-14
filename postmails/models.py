from django.conf import settings
from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    """
    Модель для хранения информации о клиентах
    """
    email = models.CharField(unique=True, max_length=100, verbose_name='Почта')
    name = models.CharField(max_length=100, verbose_name='Ф.И.О.')
    comment = models.CharField(max_length=200, verbose_name='Комментарий', **NULLABLE)
    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return f'{self.name} - {self.email} '

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ('name',)


class Message(models.Model):
    """
    Модель для хранения информации о сообщении для рассылки
    """

    title = models.CharField(max_length=255, verbose_name="Тема")
    message = models.TextField(verbose_name="Сообщение")
    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Mailing(models.Model):
    """
    Модель для хранения информации о рассылках
    """

    DAILY = "Раз в день"
    WEEKLY = "Раз в неделю"
    MONTHLY = "Раз в месяц"

    PERIODICITY_CHOICES = [
        (DAILY, "Раз в день"),
        (WEEKLY, "Раз в неделю"),
        (MONTHLY, "Раз в месяц"),
    ]

    CREATED = "Создана"
    STARTED = "Запущена"
    COMPLETED = "Завершена"

    STATUS_CHOICES = [
        (COMPLETED, "Завершена"),
        (CREATED, "Создана"),
        (STARTED, "Запущена"),
    ]

    name = models.CharField(max_length=50, verbose_name='Название рассылки')
    description = models.TextField(**NULLABLE, verbose_name='Описание', help_text='не обязательное поле')
    start_date = models.DateTimeField(help_text='(формат 05.08.2024) необязательное поле', verbose_name='Дата начала',
                                      **NULLABLE,)
    end_date = models.DateTimeField(verbose_name='Дата окончания', **NULLABLE, help_text='необязательное поле')
    next_sent_time = models.DateTimeField(verbose_name='Время следующей отправки', **NULLABLE)
    periodicity = models.CharField(max_length=150, choices=PERIODICITY_CHOICES,
                                   default=DAILY, verbose_name='Периодичность')
    status = models.CharField(max_length=150, verbose_name='Статус', choices=STATUS_CHOICES, default=CREATED)
    owner = models.ForeignKey(User, verbose_name='Владелец', on_delete=models.SET_NULL, **NULLABLE)
    clients = models.ManyToManyField(Client, related_name='mailing', verbose_name='Клиенты для рассылки')
    message = models.ForeignKey(Message, verbose_name='Cообщение', on_delete=models.CASCADE, **NULLABLE)


    def __str__(self):
        return f'{self.name}, статус: {self.status}'

    def save(
        self, *args, **kwargs
    ):
        if not self.next_sent_time:
            self.next_sent_time = self.start_date
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ("name",)
        permissions = [
            ('deactivate_mailing', 'Can deactivate mailing'),
            ('view_all_mailings', 'Can view all mailings'),
        ]


class Log(models.Model):
    """
    Модель для хранения информации о попытках рассылок
    """
    SUCCESS = 'Успешно'
    FAIL = 'Неуспешно'
    STATUS_VARIANTS = [
        (SUCCESS, 'Успешно'),
        (FAIL, 'Неуспешно'),
    ]

    time = models.DateTimeField(
        verbose_name="Дата и время попытки отправки", auto_now_add=True
    )
    status = models.CharField(max_length=50, choices=STATUS_VARIANTS, verbose_name='Cтатус рассылки')
    server_response = models.CharField(
        max_length=150, verbose_name="Ответ сервера почтового сервиса", **NULLABLE
    )
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name="Рассылка")

    def __str__(self):
        return f"{self.mailing} {self.time} {self.status} {self.server_response}"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"