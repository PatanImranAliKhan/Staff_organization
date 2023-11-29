from django.db import models
from authenticate_app.models import Location

# Create your models here.

class HR(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=30,unique=True,blank=False, primary_key=True)
    mobile = models.BigIntegerField()
    address = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    password = models.CharField(max_length=30)

    def __str__(self):
         return self.email