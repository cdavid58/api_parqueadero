from django.http import HttpResponse, JsonResponse, FileResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.db import IntegrityError
from .models import Schedule, Range_Fee, Consecutive
from car.models import Car
from parking_lot.models import Parking_Lot
from user.models import User
from datetime import datetime
from history.models import History_Schedule
from from_number_to_letters import Thousands_Separator
import pytz

tarifa = 0

def isNumeric(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def Hour():
	colombia_tz = pytz.timezone('America/Bogota')
	hora_actual_colombia = datetime.now(colombia_tz)
	formato = '%H:%M'
	return hora_actual_colombia.strftime(formato)


@api_view(['GET'])
def Get_Range_Fee(request):
	return Response([
		{
			'time':[i.start,i.end],
			'price': i.price
		}
		for i in Range_Fee.objects.all()
	])

@api_view(['POST'])
def Operations_Schedule(request):
	data = request.data
	car = None
	schedule = None
	result = False
	delete = False
	type_car = 1 # Moto
	message = "No se creo el registro"
	try:
		car = Car.objects.get(plate = data['plate'])
		print(car)
	except Car.DoesNotExist as e:
		car = None
		print(e)

	if car is None:
		if isNumeric(data['plate'][-1]):
			type_car = 2 # Carro

		car = Car(
			plate = data['plate'],
			type_car = type_car,
			parking_lot = Parking_Lot.objects.get(name = data['parking_lot'])
		)
		try:
			car.save()
		except IntegrityError as e:
			print(e)
	
	try:
		schedule = Schedule.objects.get(cart = car)
	except Schedule.DoesNotExist:
		schedule = None

	print(schedule)
	
	if schedule is None:
		c = Consecutive.objects.get(parking_lot = Parking_Lot.objects.get(name = data['parking_lot']))
		schedule = Schedule(
				consecutive = c.number,
				active = True,
				cart = car,
				user = User.objects.get(user_name = data['pk_user'].lower()),
				parking_lot = Parking_Lot.objects.get(name = data['parking_lot']),
				helmet = data['helmet'] if type_car == 1 else 0,
				note = data['note'],
				entrance = datetime.now(),
				exit = datetime.now()
			)
		schedule.save()
		c.number += 1
		c.save()
		message = f"Ingreso el vehiculo de placa {data['plate']}"
		result = True

	elif schedule is not None and schedule.active:
		schedule.active = False
		schedule.exit = datetime.now()
		schedule.save()
		# print(schedule.exit)
		# print(schedule.entrance)
		# price = Get_Price(int((schedule.exit - schedule.entrance).total_seconds() / 60 ))
		History_Schedule(
			entrance = schedule.entrance,
			exit = schedule.exit,
			cart = schedule.cart,
			user = schedule.user,
			parking_lot = schedule.parking_lot,
			total = 0
		).save()
		message = f"Salio el carro de placa {data['plate']}"
		result = True
	return Response({'result': result, 'message': message})


@api_view(['GET'])
def GET_LIST(request):	
	return Response([
		{
			'entrance': Hour(),
			'date_entrance': i.exit.strftime('%d/%m/%Y'),
			'date_exit': i.exit.strftime('%d/%m/%Y') if i.exit.strftime('%H:%M') != i.entrance.strftime('%H:%M') else 'Aún no sale',
			'entrance': i.entrance.strftime('%H:%M'),
			'exit': i.exit.strftime('%H:%M') if i.exit.strftime('%H:%M') != i.entrance.strftime('%H:%M') else 'Aún no sale',
			'plate':i.cart.plate,
			'type_car':'Carro' if int(i.cart.type_car) == 2 else 'Moto',
			'date':i.entrance.strftime('%d-%m-%Y'),
			'total':(i.exit - i.entrance).total_seconds() / 60,
			"helmet" : i.helmet,
			'note':i.note if i.note is not None else 'No tiene'
		}
		for i in Schedule.objects.all().order_by('-pk')
	])


def Get_Price(_minutes):
	global tarifa
	minutes = _minutes
	found_range = None
	price_to_charge = None
	ranges_list = [
		{
			'time':[i.start,i.end],
			'price': i.price
		}
		for i in Range_Fee.objects.all()
	]
	for r in ranges_list:
	    if r['time'][0] <= minutes <= r['time'][1]:
	        found_range = r
	        price_to_charge = r['price']
	        tarifa = price_to_charge
	        break

	if found_range:
	    return price_to_charge
	else:
	    return 0



@api_view(['GET'])
def Get_Last_Record(request):
	global tarifa
	i = Schedule.objects.get(cart = Car.objects.get(plate=request.data['plate']))
	price = 0
	hora_formateada = 0
	if not i.active:
		Schedule.objects.get(cart = Car.objects.get(plate=request.data['plate'])).delete()
		price = Get_Price(int((i.exit - i.entrance).total_seconds() / 60 ))
		m = (i.exit - i.entrance).total_seconds() / 60
		horas = int(m // 60)
		minutos = int(m % 60)
		hora_formateada = "{:02d}:{:02d}{}".format(horas % 12, minutos,"Hrs")
		


	return Response({
		'entrance': Hour(),
		'date_entrance': i.exit.strftime('%d/%m/%Y'),
		'date_exit': i.exit.strftime('%d/%m/%Y') if i.exit.strftime('%H:%M') != i.entrance.strftime('%H:%M') else 'Aún no sale',
		'exit': Hour(),
		'plate':i.cart.plate.upper(),
		'type_car':'Carro' if int(i.cart.type_car) == 2 else 'Moto',
		'date':i.entrance.strftime('%d-%m-%Y'),
		'total':Thousands_Separator(round(price)),
		"helmet" : i.helmet,
		'note':i.note if i.note is not None else 'No tiene',
		'user':i.user.user_name.capitalize(),
		"total_minutes":hora_formateada,
		"tarifa":tarifa
	})