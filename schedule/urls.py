from django.conf.urls import url
from .views import *

urlpatterns=[
	url(r'^Operations_Schedule/$',Operations_Schedule,name="Operations_Schedule"),
	url(r'^GET_LIST/$',GET_LIST,name="GET_LIST"),
	url(r'^Get_Last_Record/$',Get_Last_Record,name="Get_Last_Record"),
	url(r'^Get_Range_Fee/$',Get_Range_Fee,name="Get_Range_Fee"),
]