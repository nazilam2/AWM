
# gas_station/urls.py

from django.urls import path
from .views import search_gas_stations

urlpatterns = [
    # path('', search_gas_stations, name='search_gas_stations'),  # Update to handle the search at root
    path("", search_gas_stations, name="search_gas_stations"), 
]





