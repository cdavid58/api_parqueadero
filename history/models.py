from django.db import models
from car.models import Car
from user.models import User
from parking_lot.models import Parking_Lot
from datetime import datetime

class History_Schedule(models.Model):
	entrance = models.DateTimeField()
	exit = models.DateTimeField()
	cart = models.ForeignKey(Car, on_delete= models.CASCADE)
	user = models.ForeignKey(User, on_delete= models.CASCADE)
	parking_lot = models.ForeignKey(Parking_Lot, on_delete= models.CASCADE)
	active = models.BooleanField(default = False)

	def Calculate_Amount(self):
		entrance = datetime.fromisoformat(str(self.entrance))
		exit = datetime.fromisoformat(str(self.exit))
		return round((entrance - exit).total_seconds() / 60)