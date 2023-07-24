from django.db import models

class Car(models.Model):
	plate = models.CharField(max_length = 10, unique = True)
	type_car = models.CharField(max_length = 7)

	def __str__(self):
		return self.plate



