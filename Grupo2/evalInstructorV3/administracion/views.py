import os
import hashlib
import sqlite3 as sql3
from datetime import datetime, date, timedelta
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from evalinstructor.utils import *
from dbs.dbs import *

BASE_DIR = settings.BASE_DIR
timing = datetime.today().date()


def userLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('administracion')
        else:
            messages.info(request, f'Algo no salio bien, Intentelo otra vez')
            return redirect('/')
    context = {"title": "LogIn"}
    return render(request, "administracion/login.html", context)


def userLogout(request):
    logout(request)
    return redirect('/')


def administracion(request):
    instructorescc = []

    sqlCoord = f"""SELECT * FROM Coordinadores"""
    sqlInstr = f"""SELECT * FROM Instructores"""
    sqlApren = f"""SELECT * FROM Aprendices"""
    sqlDates = f"""SELECT * FROM EvalFechas"""
    coordinaciones = call_db(sqlCoord)
    evalFechas = call_db(sqlDates)
    coordqty = len(coordinaciones)

        # Calculate dates
    startdate = evalFechas[0][0]
    endCoordination = evalFechas[0][1]
    endInstPhoto = evalFechas[0][2]
    endEvaluation = evalFechas[0][3]

    try:
        instructoresAll = call_db(sqlInstr)
        aprendqty = len(call_db(sqlApren))

        for instructorAll in instructoresAll:
            instructorescc.append(instructorAll[6])

        instrucqty = len(set(instructorescc))

        context = {'title':'Administracion', 
                    'coordinaciones':coordinaciones, 
                    'startdate':startdate, 
                    'endCoordination':endCoordination, 
                    'endInstPhoto':endInstPhoto,
                    'endEvaluation':endEvaluation,
                    'coordqty':coordqty,
                    'instrucqty':instrucqty,
                    'aprendqty':aprendqty }
        return render(request, 'administracion/administracion.html', context)
    except:
        context = {'title':'Administracion', 
                    'coordinaciones':coordinaciones, 
                    'startdate':startdate, 
                    'endCoordination':endCoordination, 
                    'endInstPhoto':endInstPhoto,
                    'endEvaluation':endEvaluation,
                    'coordqty':coordqty,}
        return render(request, 'administracion/administracion.html', context)
