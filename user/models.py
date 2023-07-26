from django.db import models
from parking_lot.models import Parking_Lot

class User(models.Model):
	user_name = models.CharField(max_length=20,unique=True)
	psswd = models.CharField(max_length=20)
	type_user = models.IntegerField(default=3)
	parking_lot = models.ForeignKey(Parking_Lot, on_delete = models.CASCADE, null= True, blank = True)

	def __str__(self):
		return self.user_name

