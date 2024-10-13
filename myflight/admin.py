from django.contrib import admin
from .models import Flights, Airports,Passenger

# Register your models here.
admin.site.register(Flights)
admin.site.register(Airports)
admin.site.register(Passenger)