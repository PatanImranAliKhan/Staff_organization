from django.db import models

# Create your models here.

class Region(models.Model):
    regId = models.AutoField(primary_key=True)
    regName = models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.regId)
    
    
class Country(models.Model):
    conId = models.AutoField(primary_key=True)
    conName = models.CharField(max_length=50)
    regId = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.conId)


class Location(models.Model):
    locId = models.AutoField(primary_key=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=15)
    conid = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)

    def __str__(self):
            return str(self.locId)