# -*- coding: utf-8 -*-
from django.db.models import Q
from tastypie.authorization import Authorization
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie.resources import ModelResource

from airport.models import Fly, Flight, City, Status


def get_foreign(resource_calss, query_set):
    """
    Выполнение полной дегидрации объектов
    :param resource_calss: класс ресурса
    :param query_set: набор объектов для дегидрации
    :return:
    """
    resource = resource_calss()
    res = {'objects': []}
    for obj in query_set:
        bundle = resource.build_bundle(obj=obj)
        dehydrate_obj = resource.full_dehydrate(bundle)
        res['objects'].append(dehydrate_obj)
    return res


class FlightResource(ModelResource):
    """
    Ресурс "Рейсы"
    """

    class Meta:
        authorization = Authorization()
        queryset = Flight.objects.all()  # .filter(flight__arr_dep=0)
        resource_name = 'flight'

    def dehydrate(self, bundle):
        """
        Раскрытие входящих объектов связанных через внешний ключ
        :param bundle:
        :return:
        """
        bundle.data['direction_from'] = get_foreign(CityResource, City.objects.filter(pk=bundle.obj.direction_from.pk))
        bundle.data['direction_to'] = get_foreign(CityResource, City.objects.filter(pk=bundle.obj.direction_to.pk))
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


class FlyArrivalResource(ModelResource):
    """
    Ресурс "Перелеты"
    """

    class Meta:
        authorization = Authorization()
        queryset = Fly.objects.all()  # .filter(flight__arr_dep=0)
        resource_name = 'arrivals'
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
        bundle.data['flight'] = get_foreign(FlightResource, Flight.objects.filter(pk=bundle.obj.flight.pk))
        bundle.data['status'] = get_foreign(StatusResource, Status.objects.filter(pk=bundle.obj.status.pk))
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
        base_object_list = super(FlyArrivalResource, self).apply_filters(request, applicable_filters)

        arr_or_dep = request.GET.get('arr_or_dep', None)
        status = request.GET.get('status', None)
        city = request.GET.get('city', None)
        flight = request.GET.get('flight', None)

        if arr_or_dep and arr_or_dep == '':
            arr_or_dep = None
        if status and status == '':
            status = None
        if city and city == '':
            city = None
        if flight and flight == '':
            flight = None

        if arr_or_dep and base_object_list:
            if arr_or_dep in ['arr', 'dep']:
                if arr_or_dep == 'arr':
                    qt = Q(flight__arr_dep=0)
                else:
                    qt = Q(flight__arr_dep=1)
                base_object_list = base_object_list.filter(qt).distinct()
            else:
                return []

        if status and base_object_list:
            qs = Q(status__name__icontains=status)
            base_object_list = base_object_list.filter(qs).distinct()
        if city and base_object_list:
            qc = Q(flight__direction_from__name__icontains=city)
            base_object_list = base_object_list.filter(qc).distinct()
        if flight and base_object_list:
            qf = Q(flight__name__icontains=flight)
            base_object_list = base_object_list.filter(qf).distinct()

        return base_object_list
