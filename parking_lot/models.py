from django.db import models

class Parking_Lot(models.Model):
	name = models.CharField(max_length = 50)
	ability = models.IntegerField()