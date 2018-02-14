from django.contrib import admin
from .models import *

admin.site.register([Type_fly, Status, Gate, Flight, City, Fly, ])
