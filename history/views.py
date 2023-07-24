from django.http import HttpResponse, JsonResponse, FileResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.db import IntegrityError
from .models import * 

@api_view(['GET'])
def Get_History(request):
	return Response(
		[
			{
				'entrance': i.entrance.strftime('%H:%M'),
				'date_entrance': i.entrance.strftime('%d/%m/%Y'),
				'date_exit': i.exit.strftime('%d/%m/%Y'),
				'exit': i.exit.strftime('%H:%M'),
				'plate':i.cart.plate,
				'type_car':'Carro' if int(i.cart.type_car) == 2 else 'Moto',
				'date':i.entrance.strftime('%d-%m-%Y'),
				'total': (round(float((i.exit - i.entrance).total_seconds() / 60)) if i.exit > i.entrance else round(float((i.entrance - i.exit).total_seconds() / 60))) * (1500 / 60),
				'user':i.user.user_name.capitalize()
			}
			for i in History_Schedule.objects.all()
		])



