import requests
from django.core.management.base import BaseCommand
from gas_station.models import GasStation
from django.contrib.gis.geos import Point
import logging

# Set up logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Load gas stations from Overpass API for all of Ireland'

    def handle(self, *args, **options):
        overpass_url = "http://overpass-api.de/api/interpreter"
        
        # Updated query for all gas stations in Ireland
        query = """
        [out:json];
        area["ISO3166-1"="IE"][admin_level=2];  // Ireland's boundary
        node(area)["amenity"="fuel"];
        out body;
        """

        try:
            response = requests.get(overpass_url, params={'data': query})
            data = response.json()

            # Check if 'elements' exists in the response
            if 'elements' not in data or not data['elements']:
                logger.warning('No gas stations found in the response.')
                self.stdout.write(self.style.WARNING('No gas stations found in the response.'))
                return

            for station in data['elements']:
                # Extract data for each gas station
                name = station.get('tags', {}).get('name', 'Unnamed Station')
                address = station.get('tags', {}).get('addr:street', 'Unknown Address')
                latitude = station.get('lat')
                longitude = station.get('lon')

                # Ensure valid coordinates are present
                if latitude is None or longitude is None:
                    logger.warning(f"Station {name} does not have valid latitude or longitude.")
                    continue

                point = Point(longitude, latitude)  # Longitude, then latitude

                # Log and save each station in the database
                logger.info(f"Saving gas station: {name}, {address}, {latitude}, {longitude}")
                
                GasStation.objects.update_or_create(
                    name=name,
                    defaults={
                        'address': address,
                        'location': point,
                        'current_price': 0.00,  # Placeholder for price
                        'user_rating': None,    # Placeholder for rating
                        'reviews': ''           # Placeholder for reviews
                    }
                )
            self.stdout.write(self.style.SUCCESS('Gas stations loaded successfully for all of Ireland'))
        except Exception as e:
            logger.error(f"Error loading gas stations: {e}")
            self.stdout.write(self.style.ERROR(f"Error loading gas stations: {e}"))
