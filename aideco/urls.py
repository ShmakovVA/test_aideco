"""
aideco URL Configuration
"""
from django.conf.urls import url, include
from django.contrib import admin
from tastypie.api import Api

from airport.api.resources import FlyResource
from airport.utils.fill_db import test_fill
from airport.views import board, home

v1_api = Api(api_name='v1')
v1_api.register(FlyResource())

urlpatterns = [
    url('admin/', admin.site.urls),

    url(r'^test_fill/$', test_fill, name='fill_db'),

    url(r'api/', include(v1_api.urls)),

    url(r'^board/(?P<arr_or_dep>[0-1]{1})$', board, name='board'),

    url(r'^', home, name='home'),
]
