# Generated by Django 5.1.2 on 2024-11-05 00:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("gas_station", "0005_profile"),
    ]

    operations = [
        migrations.DeleteModel(name="Profile",),
    ]