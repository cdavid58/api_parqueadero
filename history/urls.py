from django.conf.urls import url
from .views import *

urlpatterns=[
	url(r'^Get_History/$',Get_History,name="Get_History"),
]