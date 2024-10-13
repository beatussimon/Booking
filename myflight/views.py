from django.shortcuts import render,redirect
from django.http import Http404
from .models import Flights, Passenger

# Create your views here.

flights = Flights.objects.all() 

def index(request):
    return render(request, "myflight/index.html", {
        "flights": flights
    })

def details(request, flight_id):
    try:
        flight = Flights.objects.get(pk=flight_id)
    except Flights.DoesNotExist:
        raise Http404("Flight not found")
    
    passengers = flight.passengers.all()
    return render(request, "myflight/details.html", {
        "flight":flight,
        "passengers":passengers
    })

def book(request, flight_id):
    flight = Flights.objects.get(pk = flight_id)
    if(request.method == "POST"):
        username = request.POST.get("username")
        try:
            passenger = Passenger.objects.get(username = username)
        except Passenger.DoesNotExist:
            return render(request, "myflight/book.html", {
                "message": "The passenger does not exist", 
                "flight": flight                
                })
        
        flight.passengers.add(passenger)
        flight.save()

        return redirect("details",flight_id = flight.id)
    
    else:
        return render(request, "myflight/book.html", {
            "flight": flight
        })