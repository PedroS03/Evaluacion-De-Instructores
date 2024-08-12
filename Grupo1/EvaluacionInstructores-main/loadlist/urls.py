from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import *


urlpatterns = [
    path('loadings', loadings, name='loadings'),
    path('loadInstructores', loadInstructores, name='loadInstructores'),
    path('loadPicture', loadPicture, name='loadPicture'),
    path('loadAprendicesMany', loadAprendicesMany, name='loadAprendicesMany'),
    path('loadCoordinaciones', loadCoordinaciones, name='loadCoordinaciones'),
]
