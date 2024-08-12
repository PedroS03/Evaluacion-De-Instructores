from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('loadlist.urls')),
    path('', include('administracion.urls')),
    path('', home, name='home'),
    path('acerca', acerca, name='acerca'),
    #path('close_session/', close_session, name='close_session'),

    path('pickInstructor', pickInstructor, name='pickInstructor'),
    path('testing', testing, name='testing'),
    path('saveTest', saveTest, name='saveTest'),

    path('validarHash/', validarHash, name='validarHash'),
    path('loginPage', loginPage, name='loginPage'),
    path('userLogout', userLogout, name='userLogout'),  
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# 401 Unauthorized
# 403 Forbidden
# 404 Not Found

