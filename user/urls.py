from django.conf.urls import url
from .views import *

urlpatterns=[
	url(r'^Create_User/$',Create_User,name="Create_User"),
	url(r'^Edit_User/$',Edit_User,name="Edit_User"),
	url(r'^Delete_User/$',Delete_User,name="Delete_User"),
	url(r'^Login/$',Login,name="Login"),
	url(r'^List_User/$',List_User,name="List_User"),
	url(r'^Get_User/$',Get_User,name="Get_User"),]