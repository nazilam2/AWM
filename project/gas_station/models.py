# gas_station/models.py
from django.contrib.gis.db import models
from django.contrib.gis.db import models
from django.contrib.auth import get_user_model

class GasStation(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    user_rating = models.FloatField(null=True)
    reviews = models.TextField(blank=True)
    location = models.PointField(null=True)
    # location = models.PointField()  # Use PostGIS PointField

    def __str__(self):
        return self.name

