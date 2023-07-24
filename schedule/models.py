from django.db import models
from car.models import Car
from user.models import User
from parking_lot.models import Parking_Lot

class Range_Fee(models.Model):
	start = models.IntegerField()
	end = models.IntegerField()
	price = models.IntegerField()

	def __str__(self):
		return 'Horas -> '+str(self.start)+' - '+str(self.end)+' | Precio: '+str(self.price)

class Schedule(models.Model):
	entrance = models.DateTimeField(auto_now_add=True)
	exit = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default = True)
	cart = models.ForeignKey(Car, on_delete= models.CASCADE)
	user = models.ForeignKey(User, on_delete= models.CASCADE,null=True,blank=True)
	parking_lot = models.ForeignKey(Parking_Lot, on_delete= models.CASCADE,null=True,blank=True)
	helmet = models.IntegerField(default = 0)
	note = models.TextField(null= True, blank = True)

	def __str__(self):
		return self.cart.plate+' '+self.user.user_name+' '+self.parking_lot.name



# x = 64
# range = [[0,60],[61,120],[121,180]
# como en que rango esta x