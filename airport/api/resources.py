from django.conf.urls import url
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

from airport.models import Fly


class FlyArrivalResource(ModelResource):
    class Meta:
        authorization = Authorization()
        queryset = Fly.objects.all().filter(flight__arr_dep=0)
        resource_name = 'arrivals'

    def prepend_urls(self):
        """
        bind "process" to url
        :return:
        """
        return [url(r'^arrivals/$', self.wrap_view('process'))]

    def process(self, request, **kwargs):
        """
        Got request arrivals with filter params (city name and/or flyght name).
        :param request:
        :param kwargs:
        :return:
        """
        self.method_check(request, allowed=['get'])
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
        city_name = data.get('city', None)
        flyght_name = data.get('flyght', None)
        status_name = data.get('status', None)

        # if param_url:
        #     try:
        #         fly = Fly.objects.get(url=data.get('url', ''))
        #     except Fly.DoesNotExist:
        #         fly = Fly(click_count=0, url=param_url, hash=hash(param_url))
        #         fly.save()
        #         return self.create_response(request, {'hash': fly.hash})
        #     return self.create_response(request, {'hash': fly.hash})
        # else:
        #     try:
        #         fly = Link.objects.get(hash=data.get('hash', ''))
        #     except Link.DoesNotExist:
        #         return self.create_response(request, {'error': 'DoesNotExist'})
        #     fly.inc_clicks()
        #     return self.create_response(request, {'url': fly.url})

class FlyDepartureResource(ModelResource):
    class Meta:
        authorization = Authorization()
        queryset = Fly.objects.all().filter(flight__arr_dep=1)
        resource_name = 'departure'

    def prepend_urls(self):
        """
        bind "process" to url
        :return:
        """
        return [url(r'^departure/$', self.wrap_view('process'))]

    def process(self, request, **kwargs):
        """
        Got request departures with filter params (city name and/or flyght name).
        :param request:
        :param kwargs:
        :return:
        """
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
        param_url = data.get('url', None)
