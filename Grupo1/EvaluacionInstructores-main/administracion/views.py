from django.shortcuts import render, redirect
import sqlite3 as sql3
from django.http import HttpResponse
from django.utils.timezone import datetime
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import AccessTimeForm

Sqlite_destiny_path = "dbs/staff.db"


@login_required
def administracion(request):
    sqlQuery1 = f"""SELECT * FROM Evaluacion"""
    sqlQuery2 = f"""SELECT * FROM Coordinadores"""
    try:
        conn = sql3.connect(Sqlite_destiny_path)
        activaciones = conn.execute(sqlQuery1,).fetchall()
        conn.close()

        conn = sql3.connect(Sqlite_destiny_path)
        coordinaciones = conn.execute(sqlQuery2,).fetchall()
        conn.close()

        context = {'title': 'Administracion', 'activaciones':activaciones, 'coordinaciones':coordinaciones}
        return render(request, 'administracion/administracion.html', context)
    except:
        context = {'title': 'Administracion'}
        return render(request, 'administracion/administracion.html', context)


#def set_access_dates(request):
    if request.method == 'POST':
        form = AccessTimeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Cambia 'success_url' por la URL a la que quieres redirigir después de guardar.
    else:
        form = AccessTimeForm()  # Aquí se inicializa el formulario vacío
    
    return render(request, 'administracion', {'form': form})

# ERROR PAGE

def error403(request):
    return render(request, 'administracion/pageErrors/page403.html')