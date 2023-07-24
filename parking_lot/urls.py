from django.conf.urls import url
from .views import *

urlpatterns=[
	url(r'^Create_Parking/$',Create_Parking,name="Create_Parking"),
	url(r'^Edit_Parking/$',Edit_Parking,name="Edit_Parking"),
	url(r'^Delete_Parking/$',Delete_Parking,name="Delete_Parking"),
]