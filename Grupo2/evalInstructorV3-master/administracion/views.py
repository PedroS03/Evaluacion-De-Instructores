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
    instconfoto = []
    instsinfoto = []
    sqlCoord = f"""SELECT * FROM Coordinadores"""
    sqlInstr = f"""SELECT * FROM Instructores"""
    sqlApren = f"""SELECT * FROM Aprendices"""
    sqlDates = f"""SELECT * FROM EvalFechas"""
    try:
            # Coordinaciones db
        coordinaciones = call_db(sqlCoord)
        coordqty = len(coordinaciones)
            # Fechas db
        evalFechas = call_db(sqlDates)
            # Calculate dates
        startdate = evalFechas[0][0]
        endCoordination = evalFechas[0][1]
        endInstPhoto = evalFechas[0][2]
        endEvaluation = evalFechas[0][3]
        
            # Instructores db
        instructoresAll = call_db(sqlInstr)
        for instructorAll in instructoresAll:
            instructorescc.append(instructorAll[6])
            if instructorAll[12] != 'static/img/img/person.jpg':
                instconfoto.append(instructorAll[6])
            else:
                instsinfoto.append(instructorAll[6])
        instrucqty = len(set(instructorescc))
        instconfotoqty = len(set(instconfoto))
        instsinfotoqty = len(set(instsinfoto))
            # Aprendices db
        aprendqty = len(call_db(sqlApren))

        context = {'title':'Administracion', 
                    'coordinaciones':coordinaciones, 
                    'coordqty':coordqty, 
                    'startdate':startdate, 
                    'endCoordination':endCoordination, 
                    'endInstPhoto':endInstPhoto,
                    'endEvaluation':endEvaluation, 
                    'instrucqty':instrucqty,
                    'instconfotoqty':instconfotoqty,
                    'instsinfotoqty':instsinfotoqty,
                    'aprendqty':aprendqty }
        return render(request, 'administracion/administracion.html', context)
    except:
        try:
                # Coordinaciones db
            coordinaciones = call_db(sqlCoord)
            coordqty = len(coordinaciones)
                # Fechas db
            evalFechas = call_db(sqlDates)
                # Calculate dates
            startdate = evalFechas[0][0]
            endCoordination = evalFechas[0][1]
            endInstPhoto = evalFechas[0][2]
            endEvaluation = evalFechas[0][3]
                # Instructores db
            instructoresAll = call_db(sqlInstr)
            for instructorAll in instructoresAll:
                instructorescc.append(instructorAll[6])
                if instructorAll[12] != 'static/img/img/person.jpg':
                    instconfoto.append(instructorAll[6])
                else:
                    instsinfoto.append(instructorAll[6])
            instrucqty = len(set(instructorescc))
            instconfotoqty = len(set(instconfoto))
            instsinfotoqty = len(set(instsinfoto))

            context = {'title':'Administracion', 
                        'coordinaciones':coordinaciones, 
                        'coordqty':coordqty, 
                        'startdate':startdate, 
                        'endCoordination':endCoordination, 
                        'endInstPhoto':endInstPhoto,
                        'endEvaluation':endEvaluation, 
                        'instrucqty':instrucqty,
                        'instconfotoqty':instconfotoqty,
                        'instsinfotoqty':instsinfotoqty,
                        'aprendqty':"Not Setup" }
            return render(request, 'administracion/administracion.html', context)
        except:
            try:
                    # Coordinaciones db
                coordinaciones = call_db(sqlCoord)
                coordqty = len(coordinaciones)
                    # Fechas db
                evalFechas = call_db(sqlDates)
                    # Calculate dates
                startdate = evalFechas[0][0]
                endCoordination = evalFechas[0][1]
                endInstPhoto = evalFechas[0][2]
                endEvaluation = evalFechas[0][3]
                    # Crear tabla Informes
                context = {'title':'Administracion', 
                            'coordinaciones':coordinaciones, 
                            'coordqty':coordqty, 
                            'startdate':startdate, 
                            'endCoordination':endCoordination, 
                            'endInstPhoto':endInstPhoto,
                            'endEvaluation':endEvaluation, 
                            'instrucqty':"Not Setup",
                            'instconfotoqty':"Not Setup",
                            'instsinfotoqty':"Not Setup",
                            'aprendqty':"Not Setup" }
                return render(request, 'administracion/administracion.html', context)
            except:
                messages.warning(request, f'Todo parece indicar que la aplicación no ha sido activada.')
                return redirect('loadActivation')


def ready(request):
    from jobs import allSchedulers
    fullMixTable(request)
    allSchedulers.start()

    messages.info(request, f'Se creo la tabla de "Informes" y se activaron los Schedules')
    return redirect('administracion')


def createFinalReport(request):
    print("Create function")

    messages.info(request, f'Create Function createFinalReport')
    return redirect('administracion')

