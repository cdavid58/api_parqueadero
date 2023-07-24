from django.db import models

class User(models.Model):
	user_name = models.CharField(max_length=20,unique=True)
	psswd = models.CharField(max_length=20)
	type_user = models.IntegerField(default=3)

	def __str__(self):
		return self.user_name

