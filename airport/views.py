from logging import log

from django.http import HttpResponseRedirect
from django.shortcuts import render

from airport.forms import FormFilterFlights
from airport.models import Fly
from fill_db import fill_city, fill_gates, fill_status, fill_types_fly

LIM_OBJ = 20  # limit flights for board


def home(request):
    """
    Welcome page (w/o data)
    :param request:
    :return: render with title and main menu buttons
    """
    return render(request, 'common/base.html', context={})


def get_flights_context(request, arr_or_dep):
    """
    Generate context for rendering board.
    :param request: arrivals or departures request
    :param arr_or_dep: if 0 - arrivals, otherwise - departure
    :return: context for rendering "home.html" like {'form': form, 'flights': flights}
    """
    form = FormFilterFlights()
    flights = []
    if request.method == 'POST':
        try:
            form = FormFilterFlights(request.POST)
            if form.is_valid():
                flight_name = form.cleaned_data['flight_name']
                city_name = form.cleaned_data['city_name']
                status_name = form.cleaned_data['status_name']

                flights = Fly.objects.all().filter(flight__name__icontains=flight_name)
                if status_name:
                    flights = Fly.objects.all().filter(flight__fly__status=status_name)

                if arr_or_dep == 0:
                    flights = flights.filter(flight__direction_from__name__icontains=city_name)
                else:
                    flights = flights.filter(flight__direction_to__name__icontains=city_name)
        except Exception as e:
            log(0, str(e))
    else:
        flights = Fly.objects.all()
    return {'form': form,
            'flights': flights.filter(flight__arr_dep=arr_or_dep).order_by('time_from').reverse()[:LIM_OBJ]}


def arrivals(request):
    """
    Show arrivals board
    :param request:
    :return: render with context from get_flights_context
    """
    ctx = get_flights_context(request, 0)
    return render(request, 'home.html', context=ctx)


def departures(request):
    """
    Show departures board
    :param request:
    :return: render with context from get_flights_context
    """
    ctx = get_flights_context(request, 1)
    return render(request, 'home.html', context=ctx)


def test_fill(request):
    """
    Filling db with test data
    :param request:
    :return: redirect to home
    """
    fill_city()
    fill_gates()
    fill_status()
    fill_types_fly()
    return HttpResponseRedirect(r'/')
