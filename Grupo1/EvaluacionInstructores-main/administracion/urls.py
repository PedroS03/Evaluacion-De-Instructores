from django.urls import path, include
from .views import *
from .decorators import *

urlpatterns = [
    path('administracion', administracion, name='administracion'),
    path('error403', error403, name='error403'),
]
