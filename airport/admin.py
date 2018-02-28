from django.contrib import admin

from .models import *

admin.site.register([TypeFly, Status, Gate, Flight, City, Fly, ])
