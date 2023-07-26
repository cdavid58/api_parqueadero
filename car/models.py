from django.db import models
from parking_lot.models import Parking_Lot

class Car(models.Model):
	plate = models.CharField(max_length = 10, unique = True)
	type_car = models.CharField(max_length = 7)
	parking_lot = models.ForeignKey(Parking_Lot, on_delete = models.CASCADE, null= True, blank = True)

	def __str__(self):
		return self.plate



