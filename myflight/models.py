from typing import Any
from django.db import models

# Create your models here.
class Airports(models.Model):
    city = models.CharField(max_length=64, null=True)
    code = models.CharField(max_length=3, null=True)

    def __str__(self):
        return f"{self.city}({self.code})"
    
    
class Passenger(models.Model):
    username = models.CharField(max_length=64)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Flights(models.Model):
    origin = models.ForeignKey(Airports, max_length=64, on_delete=models.CASCADE, related_name="departures", null=True)
    destination = models.ForeignKey(Airports, max_length=64, on_delete=models.CASCADE, related_name="arrivals", null=True)
    duration = models.IntegerField(null=True)
    passengers = models.ManyToManyField(Passenger, blank=True, related_name="flights") 

    def __str__(self):
        return f"From {self.origin} to {self.destination} - {self.duration}"
    
    def is_flight_valid(self):
        return self.origin != self.destination or self.duration >= 0