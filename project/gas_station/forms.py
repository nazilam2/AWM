# gas_station/forms.py
from django import forms

class GasStationSearchForm(forms.Form):
    address = forms.CharField(label='Enter Address or Location', max_length=255)
    station_name = forms.CharField(label='Enter Gas Station Name (optional)', max_length=100, required=False)

