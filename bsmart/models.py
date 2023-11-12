from django.db import models

# Create your models here.

class CsvData(models.Model):
    year = models.CharField(max_length=255)
    miles = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    make = models.CharField(max_length=255)