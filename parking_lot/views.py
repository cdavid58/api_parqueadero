from django.http import HttpResponse, JsonResponse, FileResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.db import IntegrityError
from .models import Parking_Lot

@api_view(['POST'])
def Create_Parking(request):
	data = request.data
	result = False
	message = "El parqueadero no fue creo"

	try:
		parking = Parking_Lot.objects.get(name = data['name'])
		message = "El parqueadero ya existe"
	except Parking_Lot.DoesNotExist:
		parking = None

	if parking is None:
		parking = Parking_Lot(
			name = data['name'],
			ability = data['ability']
		)
		try:
			parking.save()
			result = True
			message = "Parqueadero creado con éxito"
		except IntegrityError as e:
			message = "El parqueadero ya existe"
	return Response({'result': result, 'message': message})

@api_view(['PUT'])
def Edit_Parking(request):
	data = request.data
	parking = Parking_Lot.objects.get(pk = data['pk_parking'])
	name_p = parking.name
	parking.name = data['name']
	parking.ability = data['ability']
	result = False
	try:
		parking.save()
		message = f"El parqueadero {name_p} fué actualizado con exito"
		result = True
	except Exception as e:
		message = f"Error el la actualización del parqueadero {parking.name}"
	return Response({'result': result, 'message': message})


@api_view(['DELETE'])
def Delete_Parking(request):
	data = request.data
	result = False
	try:
		Parking_Lot.objects.get(pk = data['pk_parking']).delete()
		message = "Parqueadero fue eliminado con éxito"
		result = True
	except Parking_Lot.DoesNotExist:
		message = "Error en la eliminación del parqueadero"
	return Response({'result': result, 'message': message})