# -*- coding: utf-8 -*-
from django.db import IntegrityError

from airport.models import City, Status, Gate, Type_fly

CITYES = {'Москва': 'M', 'Екатеринбург': 'E', 'Мюнхен': 'M', 'Берлин': 'Б'}
STATUSES = ['-', 'Регистрация', 'Посадка', 'Прибытие', 'Отмена', 'Задержка', 'Завершен']
GATES = ['G1', 'G2', 'G3', 'F1', 'F2', 'F3']
TYPES_FLY = ['TYPE1', 'TYPE2', 'TYPE3', 'TYPE3']


def fill_city():
    for city_name, code in CITYES.items():
        try:
            City(name=city_name, code=code).save()
        except IntegrityError:
            pass


def fill_status():
    for status_name in STATUSES:
        try:
            Status(name=status_name).save()
        except IntegrityError:
            pass

def fill_gates():
    for gate_name in GATES:
        try:
            Gate(name=gate_name).save()
        except IntegrityError:
            pass

def fill_types_fly():
    for type_fly_name in TYPES_FLY:
        try:
            Type_fly(name=type_fly_name).save()
        except IntegrityError:
            pass
