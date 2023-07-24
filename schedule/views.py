from django.http import HttpResponse, JsonResponse, FileResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.db import IntegrityError
from .models import Schedule, Range_Fee
from car.models import Car
from parking_lot.models import Parking_Lot
from user.models import User
from datetime import datetime
from history.models import History_Schedule
import pytz

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
	except Car.DoesNotExist as e:
		car = None
		print(e)

	if car is None:
		print(data['plate'][-1])
		if isNumeric(data['plate'][-1]):
			type_car = 2 # Carro

		car = Car(
			plate = data['plate'],
			type_car = type_car
		)
		try:
			car.save()
		except IntegrityError as e:
			print(e)
	
	try:
		schedule = Schedule.objects.get(cart = car)
	except Schedule.DoesNotExist:
		schedule = None
	
	if schedule is None:
		schedule = Schedule(
				active = True,
				cart = car,
				user = User.objects.get(pk = data['pk_user']),
				parking_lot = Parking_Lot.objects.get(name = data['parking_lot']),
				helmet = data['helmet'] if type_car == 1 else 0,
				note = data['note'],
				entrance = Hour(),
				exit = Hour()
			)
		schedule.save()
		print("Ya grabe",schedule)
		message = f"Ingreso el vehiculo de placa {data['plate']}"
		result = True

	elif schedule is not None and schedule.active:
		print("Voy a eliminar")
		schedule.active = False
		schedule.exit = datetime.now()
		schedule.save()
		History_Schedule(
			entrance = schedule.entrance,
			exit = Hour(),
			cart = schedule.cart,
			user = schedule.user,
			parking_lot = schedule.parking_lot
		).save()
		message = f"Salio el carro de placa {data['plate']}"
		result = True
		# schedule.delete()
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


def Get_Price(minutes):
	minutes = 62
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
	        break

	if found_range:
	    return price_to_charge
	else:
	    return 0



@api_view(['GET'])
def Get_Last_Record(request):
	i = Schedule.objects.get(cart = Car.objects.get(plate=request.data['plate']))
	price = 0

	if not i.active:
		Schedule.objects.get(cart = Car.objects.get(plate=request.data['plate'])).delete()
		price = Get_Price(int((i.exit - i.entrance).total_seconds() / 60 ))
	return Response({
		'entrance': Hour(),
		'date_entrance': i.exit.strftime('%d/%m/%Y'),
		'date_exit': i.exit.strftime('%d/%m/%Y') if i.exit.strftime('%H:%M') != i.entrance.strftime('%H:%M') else 'Aún no sale',
		'exit': Hour(),
		'plate':i.cart.plate,
		'type_car':'Carro' if int(i.cart.type_car) == 2 else 'Moto',
		'date':i.entrance.strftime('%d-%m-%Y'),
		'total':price,
		"helmet" : i.helmet,
		'note':i.note if i.note is not None else 'No tiene',
		'user':i.user.user_name.capitalize()
	})