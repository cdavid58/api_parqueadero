from django.http import HttpResponse, JsonResponse, FileResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.db import IntegrityError
from .models import User

@api_view(['POST'])
def Create_User(request):
    data = request.data
    message = "El usuario ya existe"
    result = False
    
    try:
        user = User.objects.get(user_name=data['user_name'], psswd=data['psswd'])
    except User.DoesNotExist:
        user = None
    
    if user is None:
        new_user = User(
            user_name=data['user_name'].lower(),
            psswd=data['psswd'],
            type_user=data['type_user']
        )
        try:
            new_user.save()
            message = "Usuario creado con éxito"
            result = True
        except IntegrityError as e:
            pass    
    return Response({'result': result, 'message': message})

@api_view(['PUT'])
def Edit_User(request):
	data = request.data
	user = User.objects.get(pk = data['pk_user'])
	user.user_name = data['user_name'].lower()
	user.psswd = data['psswd']
	user.type_user = data['type_user']
	result = False
	try:
		user.save()
		message = "Usuario actualizado con éxito"
		result = True
	except Exception:
		message = "Error en la actualización del usuario"
	return Response({'result': result, 'message': message})

@api_view(['DELETE'])
def Delete_User(request):
	data = request.data
	result = False
	try:
		User.objects.get(pk = data['pk_user']).delete()
		message = "Usuario eliminado con éxito"
		result = True
	except Exception:
		message = "Error en la eliminación del usuario"
	return Response({'result': result, 'message': message})


@api_view(['POST'])
def Login(request):
	data = request.data
	result = False
	message = "El usuario no existe"
	try:
		user = User.objects.get(user_name=data['user_name'].lower(), psswd=data['psswd'])
	except User.DoesNotExist:
		user = None
	if user is not None:
		result = True
		message = "Success"
	return Response({'result':result, 'message':message})























