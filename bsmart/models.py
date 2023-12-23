from django.db import models

# Create your models here.

class CsvData(models.Model):
    year = models.CharField(max_length=255)
    miles = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    make = models.CharField(max_length=255)
    
class FileStatus(models.Model):
    file_name = models.CharField(max_length=255)
    upload_timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)  # e.g., "Uploaded Successfully"

    def __str__(self):
        return self.file_name