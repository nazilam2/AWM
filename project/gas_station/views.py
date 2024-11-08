from django.shortcuts import render
from django import forms
from .models import GasStation
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
import time
import logging
from django.contrib.gis.geos import Point
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse


from django.contrib.gis.geos import Point

# Set up logging
logger = logging.getLogger(__name__)

class GasStationSearchForm(forms.Form):
    address = forms.CharField(label='Enter Address or Location', max_length=255)

def search_gas_stations(request):
    results = []
    user_location = None

    if request.method == 'POST':
        form = GasStationSearchForm(request.POST)

        if form.is_valid():
            address = form.cleaned_data.get('address')
            geolocator = Nominatim(user_agent="gas_station_locator")

            try:
                location = geocode_with_retry(geolocator, address)
                if location:
                    user_location = (location.latitude, location.longitude)
                    user_point = Point(location.longitude, location.latitude, srid=4326)
                    results = (GasStation.objects
                               .annotate(distance=Distance('location', user_point))
                               .filter(distance__lte=D(km=5))
                               .order_by('distance'))
                else:
                    form.add_error('address', 'Could not geocode the address. Please try another one.')
            except GeocoderServiceError as e:
                logger.error(f"Geocoder service error: {str(e)}")
                form.add_error('address', f'The geocoding service is currently unavailable. Please try again later. Error: {str(e)}')
            except GeocoderTimedOut:
                form.add_error('address', 'The geocoding request timed out. Please try again.')
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                form.add_error('address', f'An unexpected error occurred: {str(e)}')
    else:
        form = GasStationSearchForm()

    return render(request, 'gas.html', {
        'form': form,
        'results': results,
        'user_location': user_location
    })


def geocode_with_retry(geolocator, address, retries=3, delay=2, timeout=10):
    for attempt in range(retries):
        try:
            return geolocator.geocode(address, timeout=timeout)  # Increase the timeout
        except GeocoderTimedOut:
            logger.warning(f"Geocoding timed out for address: {address}. Attempt {attempt + 1}.")
            if attempt < retries - 1:
                time.sleep(delay)  # Wait before retrying
            else:
                raise Exception("Geocoding service timed out after multiple attempts.")
        except GeocoderServiceError as e:
            logger.error(f"Geocoder service error: {str(e)}")
            if "500" in str(e):
                if attempt < retries - 1:
                    time.sleep(delay)  # Wait before retrying
                    continue  # Retry the request
                else:
                    raise Exception("Geocoding service returned an internal server error after multiple attempts.")
            else:
                raise Exception(f"Geocoding service error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during geocoding: {str(e)}")
            raise Exception(f"An unexpected error occurred: {str(e)}")

#end of my search for gas station 

#This part is for adding user profile 

