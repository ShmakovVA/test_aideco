# -*- coding: utf-8 -*-

from django.db.models import Q
from tastypie.authorization import Authorization
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie.resources import ModelResource

from airport.api.dehydrate_utils import get_foreign_object
from airport.models import Fly, Flight, City, Status


class FlightResource(ModelResource):
    """
    Ресурс "Рейсы"
    """

    class Meta:
        authorization = Authorization()
        queryset = Flight.objects.all()
        resource_name = 'flight'

    def dehydrate(self, bundle):
        """
        Раскрытие входящих объектов связанных через внешний ключ
        :param bundle:
        :return:
        """
        bundle.data['direction_from'] = get_foreign_object(CityResource,
                                                           City.objects.filter(pk=bundle.obj.direction_from.pk))
        bundle.data['direction_to'] = get_foreign_object(CityResource,
                                                         City.objects.filter(pk=bundle.obj.direction_to.pk))
        return bundle


class CityResource(ModelResource):
    """
    Ресурс "Города"
    """

    class Meta:
        authorization = Authorization()
        queryset = City.objects.all()
        resource_name = 'city'


class StatusResource(ModelResource):
    """
    Ресурс "Статусы"
    """

    class Meta:
        authorization = Authorization()
        queryset = Status.objects.all()
        resource_name = 'status'


class FlyResource(ModelResource):
    """
    Ресурс "Перелеты"
    """

    class Meta:
        authorization = Authorization()
        queryset = Fly.objects.all()
        resource_name = 'flights'
        fields = ['id', 'time_from', 'time_to', 'comment']
        filtering = {
            'flight': ALL_WITH_RELATIONS,
            'status': ALL_WITH_RELATIONS
        }

    def dehydrate(self, bundle):
        """
        Раскрытие входящих объектов связанных через внешний ключ
        :param bundle:
        :return:
        """
        bundle.data['flight'] = get_foreign_object(FlightResource, Flight.objects.filter(pk=bundle.obj.flight.pk))
        bundle.data['status'] = get_foreign_object(StatusResource, Status.objects.filter(pk=bundle.obj.status.pk))
        return bundle

    def apply_filters(self, request, applicable_filters):
        """
        Фильтрация объектов по заданным в реквесте параметрам.
        Если фильтры не пустые, то производится фильтрация по вхождению подстроки.
        Доступные параметры:
            arr_or_dep - допустимые значения - 'arr', 'dep' (прибытия и отправления соответственно)
            status - статус
            city - направление
            flight - рейс
        :param request:
        :param applicable_filters:
        :return:
        """
        true_q = ~Q(pk=None)
        base_object_list = super(FlyResource, self).apply_filters(request, applicable_filters)

        arr_or_dep = request.GET.get('arr_or_dep', '')
        status = request.GET.get('status', '')
        city = request.GET.get('city', '')
        flight = request.GET.get('flight', '')

        if arr_or_dep == 'arr':
            q_direction = Q(flight__arr_dep=0)
        elif arr_or_dep == 'dep':
            q_direction = Q(flight__arr_dep=1)
        else:
            q_direction = true_q

        q_status = Q(status__name__icontains=status) if status else true_q
        q_city = Q(flight__direction_from__name__icontains=city) if city else true_q
        q_flight = Q(flight__name__icontains=flight) if flight else true_q

        return base_object_list.filter(q_direction & q_status & q_city & q_flight).distinct()
