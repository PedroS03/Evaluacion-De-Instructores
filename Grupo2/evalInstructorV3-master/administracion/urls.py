from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('administracion', administracion, name='administracion'),
    path('createFinalReport', createFinalReport, name='createFinalReport'),
    path('userLogin', userLogin, name='userLogin'),
    path('userLogout', userLogout, name='userLogout'),
    path('ready', ready, name='ready'),

]