"""aideco URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from tastypie.api import Api

from airport.api.resources import FlyArrivalResource, FlyDepartureResource
from airport.views import arrivals, test_fill, departures, home

v1_api = Api(api_name='v1')
v1_api.register(FlyArrivalResource())
v1_api.register(FlyDepartureResource())


urlpatterns = [
    url('admin/', admin.site.urls),

    url(r'^test_fill/', test_fill, name='fill_db'),

    url(r'^arrivals/', arrivals, name='a'),
    url(r'^departures/', departures, name='d'),
    url(r'^', home, name='h'),

]
