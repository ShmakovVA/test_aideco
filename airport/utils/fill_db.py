# -*- coding: utf-8 -*-
from django.db import IntegrityError
from django.http import HttpResponseRedirect

from airport.models import City, Status, Gate, TypeFly

CITYES = {'Москва': 'M', 'Екатеринбург': 'E', 'Мюнхен': 'M', 'Берлин': 'Б'}
STATUSES = ['Регистрация', 'Посадка', 'Прибытие', 'Отмена', 'Задержка', 'Завершен']
GATES = ['G1', 'G2', 'G3', 'F1', 'F2', 'F3']
TYPES_FLY = ['TYPE1', 'TYPE2', 'TYPE3', 'TYPE3']


def safety_save(model, *args):
    try:
        model(None, *args).save()
    except IntegrityError:
        pass


def fill_city():
    for city_name, code in CITYES.items():
        safety_save(City, city_name, code)


def fill_status():
    for status_name in STATUSES:
        safety_save(Status, status_name)


def fill_gates():
    for gate_name in GATES:
        safety_save(Gate, gate_name)


def fill_types_fly():
    for type_fly_name in TYPES_FLY:
        safety_save(TypeFly, type_fly_name)


def test_fill(request):
    """
    Заполнение тестовыми данными БД
    :return: перенаправление на стартовую
    """
    fill_city()
    fill_gates()
    fill_status()
    fill_types_fly()
    return HttpResponseRedirect(r'/')
