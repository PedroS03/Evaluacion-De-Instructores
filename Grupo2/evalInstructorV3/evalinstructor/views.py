import os
import sqlite3 as sql3
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from dbs.dbs import call_db, call_db_one

BASE_DIR = settings.BASE_DIR


def home(request):
    end_date = []
    sqlQuery = f"""SELECT * FROM Coordinadores"""
    try:
        coordinaciones = call_db(sqlQuery)
        end_date = coordinaciones[0][6]

        context = {"title": "SENA - Evaluación de instructores", "end_date": end_date}
        return render(request, "evalinstructor/home.html", context)
    except:
        messages.warning(request, f'No se encontro la Base de Datos')
        context = {"title": "Subir Archivo de Activación"}
        return render(request, "loadlists/loadActivation.html", context)


def validarHash(request):
    if request.method == 'POST':
        hash = request.POST.get('hash')
        sqlCoord = f"""SELECT * FROM Coordinadores WHERE HASH =?"""
        sqlInstr = f"""SELECT * FROM Instructores WHERE HASH =?"""
        sqlApren = f"""SELECT * FROM Aprendices WHERE HASH =?"""
            # Coordinacion
        try:
            coordinador = call_db_one(sqlCoord, hash)
            if coordinador[8] == 'coordinador':
                context = {"title": "Subir Listas", "coordinador":coordinador}
                return render(request, "loadlists/loadings.html", context)
            else:
                messages.warning(request, f'El registro del Coordinador no se encontro, por favor verificar con verifique con el Centro de Producción de Soluciones Inteligentes.')
                return redirect('home')
        except:
                # Instructor
            try:
                instructor = call_db_one(sqlInstr, hash)
                if instructor[10] == 'instructor':
                    context = {"title": "Subir Foto", "instructor":instructor}
                    return render(request, "loadlists/uploadPhoto.html", context)
                else:
                    messages.warning(request, f'El registro del instructor no se encontro, por favor verificar con su coordinación.')
                    return redirect('home')
            except:
                    # Aprendiz
                try:
                    aprendiz = call_db_one(sqlApren, hash)
                    if aprendiz[10] == 'aprendiz':
                        context = {"title": "Subir Listas", "aprendiz":aprendiz}
                        return HttpResponse("APRENDICES ARE READY", aprendiz)
                    else:
                        messages.warning(request, f'El registro del aprendiz no se encontro, por favor verificar con su instructor.')
                        return redirect('home')
                except:
                    messages.warning(request, f'El hash ingresado no se encontro, intentelo otra vez')
                    return redirect('home')
