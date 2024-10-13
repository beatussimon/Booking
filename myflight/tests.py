from django.test import TestCase,Client
from .models import Airports, Flights, Passenger
from django.db.models import Max 

# Create your tests here.

class FlightTestCase(TestCase):
    def setUp(self):
        a1 = Airports.objects.create(city="Ngara", code="AAA" )
        a2 = Airports.objects.create(city="german", code="BBB")

        Flights.objects.create(origin=a1, destination=a2, duration=100)
        Flights.objects.create(origin=a2, destination=a2, duration=200)
        Flights.objects.create(origin=a2, destination=a1, duration=100)

    def test_departures_count(self):
        a= Airports.objects.get(code="AAA")
        self.assertEqual(a.departures.count(),1)
    
    def test_arrivals_count(self):
        a = Airports.objects.get(code="BBB")
        self.assertEqual(a.arrivals.count(),2)
    
    def test_is_flight_valid(self):
        a1 = Airports.objects.get(code="AAA" )
        a2 = Airports.objects.get(code="BBB")
        f= Flights.objects.get(origin=a1, destination=a2, duration=100)

        self.assertTrue(f.is_flight_valid())
    
    def test_is_flight_invalid(self):
        a1 = Airports.objects.get(code="AAA" )
        f= Flights.objects.create(origin=a1, destination=a1, duration=100)

        self.assertFalse(f.is_flight_valid())
    
    def test_duration_valid(self):
        a1 = Airports.objects.get(code="AAA" )
        a2 = Airports.objects.get(code="BBB")
        f= Flights.objects.create(origin=a1, destination=a2, duration=-100)

        self.assertFalse(f.is_flight_valid())

    def test_index(self):
        c= Client()
        response = c.get("/myflight/")
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.context["flights"].count(),3)

    def test_validflight_page(self):
        a1= Airports.objects.get(code="AAA")
        a2 = Airports.objects.get(code="BBB")
        flight= Flights.objects.get(origin=a1, destination=a2)

        c=Client()
        response = c.get(f"/myflight/{flight.id}/")
        self.assertEqual(response.status_code, 200)

    def test_invalid_flight_page(self):
        max_id = Flights.objects.all().aggregate(Max("id"))["id__max"] or 0

        c=Client()
        response= c.get(f"/myflight/{max_id+1}/")
        self.assertEqual(response.status_code, 404)

    def test_flight_page_passengers(self):
        p= Passenger.objects.create(first_name="Beaus", last_name="Belarus")
        f= Flights.objects.get(pk=1)
        f.passengers.add(p)

        c = Client()
        response = c.get(f"/myflight/{f.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["passengers"].count(), 1)

    def test_flight_page_non_passengers(self):
        a1= Airports.objects.get(code="AAA")
        f = Flights.objects.create(origin=a1, destination=a1, duration=120)

        c = Client()
        response = c.get(f"/myflight/{f.id}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn('passengers', response.context)
        self.assertEqual(response.context["passengers"].count(), 0) 