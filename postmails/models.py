from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.CharField(unique=True, verbose_name='Почта')
    name = models.CharField(max_length=100, verbose_name='Ф.И.О.')
    comment = models.CharField(max_length=200, verbose_name='комментарий', **NULLABLE)

    def __str__(self):
        return f'{self.name} - {self.email} '

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Mailing(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название рассылки')
    sent_date = models.DateField(auto_now_add=True, verbose_name='Дата')
    sent_time = models.TimeField(auto_now_add=True, verbose_name='Время')
    periodicity = models.CharField(max_length=50, verbose_name='Периодичность')
    status = models.CharField(max_length=50, verbose_name='Статус')
    is_active = models.BooleanField(default=True, verbose_name="Действующая")


    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'