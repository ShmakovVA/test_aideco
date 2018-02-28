# -*- coding: utf-8 -*-
from logging import log

from django.db.models import Q
from django.shortcuts import render_to_response, render

from airport.forms import FormFilterFlights
from airport.models import Fly

LIM_OBJ = 20  # количество объектов на табло


def get_flights(form, arr_or_dep):
    """
    Получение данных о прилетах/отправлениях
    :param form: форма с фильтрами для вывода
    :param arr_or_dep: если = 0 - прибытие, иначе - отправление
    :return: контекст для рендера страницы в виде {'form': form, 'flights': flights}
    """
    if form.is_valid():
        flight_name = form.cleaned_data['flight_name']
        city_name = form.cleaned_data['city_name']
        status_name = form.cleaned_data['status_name']

        q_flight = Q(flight__name__icontains=flight_name)
        q_status = Q(flight__fly__status=status_name)
        if arr_or_dep == '0':
            q_city = Q(flight__direction_from__name__icontains=city_name)
        else:
            q_city = Q(flight__direction_to__name__icontains=city_name)

        return Fly.objects.all().filter(q_city & q_flight & q_status)
    else:
        return [], "Не валидная форма"


def home(request):
    """
    Приветственный экран
    :param request:
    :return: рендер приветственного экрана
    """
    return render_to_response('common/base.html')


def board(request, arr_or_dep=0):
    """
    Показ рейсов
    :param request:
    :param arr_or_dep: фильтр для прибытия/отправления
    :return: рендер с контекстом get_flights_context
    """
    form = FormFilterFlights()
    flights = Fly.objects.all()

    if request.method == 'POST':
        try:
            form = FormFilterFlights(request.POST)
            flights = get_flights(form, arr_or_dep)
        except Exception as e:
            log(0, str(e))

    ctx = {'form': form,
           'flights': flights.filter(flight__arr_dep=arr_or_dep).order_by('time_from').reverse()[:LIM_OBJ]}

    return render(request, 'board.html', context=ctx)
