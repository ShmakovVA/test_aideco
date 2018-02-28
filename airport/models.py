# -*- coding: utf-8 -*-
from django.db import models


# Каталоги (Города, Выходы, ...)

class City(models.Model):
    """
    Города
    """
    name = models.CharField(max_length=100, blank=False, null=False, unique=True, verbose_name=u'Город')
    code = models.CharField(max_length=4, blank=True, null=True, verbose_name=u'Код')

    def __str__(self):
        return '{} [{}]'.format(self.name, self.code)

    class Meta:
        verbose_name = "Города"


class Status(models.Model):
    """
    Статусы
    """
    name = models.CharField(max_length=20, blank=False, null=False, unique=True, verbose_name=u'Статус')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = "Статусы"


class Gate(models.Model):
    """
    Выходы
    """
    name = models.CharField(max_length=10, blank=False, null=False, unique=True, verbose_name=u'Выход')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = "Выходы"


class TypeFly(models.Model):
    """
    Типы ВС
    """
    name = models.CharField(max_length=25, blank=False, null=False, unique=True, verbose_name=u'Тип ВС')

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = "Типы ВС"


class Flight(models.Model):
    """
    Рейсы (название, направление, счетчик завершенных перелетов)
    """
    name = models.CharField(max_length=25, blank=False, null=False, unique=True, verbose_name=u'Рейс')
    direction_from = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name=u'Из', related_name='from_city')
    direction_to = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name=u'В', related_name='to_city')
    arr_dep = models.PositiveSmallIntegerField(verbose_name=u'Вылет/Прилет (1/0)', default=0)
    counter = models.IntegerField(default=0, verbose_name=u'Количество завершенных (автоинкремент)')

    def increment(self):
        self.counter += 1
        self.save()

    def __str__(self):
        return '[{}]_________[{} - {}]______________{}'.format(self.name, self.direction_from, self.direction_to,
                                                               self.counter)

    class Meta:
        verbose_name = "Рейсы"


# Перелеты

class Fly(models.Model):
    """
    Перелеты с параметрами и в соответствии рейсу
    """
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, verbose_name=u'Рейс')
    gate = models.ForeignKey(Gate, on_delete=models.CASCADE, verbose_name=u'Выход', blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, verbose_name=u'Статус', blank=True, null=True)
    fly_type = models.ForeignKey(TypeFly, on_delete=models.CASCADE, verbose_name=u'Тип ВС', blank=True, null=True)
    time_from = models.DateTimeField(verbose_name=u'Время')
    time_to = models.DateTimeField(verbose_name=u'Время (фактическое)', blank=True, null=True)
    comment = models.CharField(max_length=100, blank=True, null=True, verbose_name=u'Комментарий')

    def __init__(self, *args, **kwargs):
        """
        Определение был ли ранее завершен перелет
        """
        super().__init__(*args, **kwargs)
        self.was_closed = False
        if self.status:
            self.was_closed = self.status.name == u'Завершен'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """
        Выполнение после сохранения проверки на завершение перелета и если мы завершили перелет,
        то увеличиваем счетчик для рейса
        """
        super(Fly, self).save()
        if self.status and not self.was_closed and self.status.name == u'Завершен':
            self.flight.increment()

    def __str__(self):
        return '{}  |  {}  |  {}  |  {}  |  {}  |  {}'.format(self.flight, self.time_from, self.time_to, self.gate,
                                                              self.status,
                                                              self.comment)

    class Meta:
        verbose_name = "Перелеты"
