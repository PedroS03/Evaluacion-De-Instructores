import os
import csv
import sqlite3 as sql3
import pandas as pd
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime, timezone
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import LogInForm, preguntasForm
from loadlist.models import Instructor, Aprendiz, Evaluacion, Coordinador
from loadlist.utils import semestre, crearTestingFolder

# Folder to sqlite3
Sqlite_destiny_path = "dbs/staff.db"
testing_destiny_path = "csvs/ltest/"


def home(request):
    context = {"title": "SENA - Evaluación de instructores"}
    return render(request, 'evalinst/home.html', context)

def close_session(request):
    request.session.flush()
    messages.success(request, "Has cerrado sesión.")
    return redirect('home')

def acerca(request):
    context = {"title" : "SENA - CPSI"}
    return render(request, 'evalinst/acerca.html', context)

def validarHash(request):
    request.session.create()
    request.session['getAprend'] = []
    request.session['allInstructores'] = []
    
    if request.method == 'POST':
        allInstructores = []
        hash = request.POST.get('hash')

        # Coordinadores
        conn = sql3.connect(Sqlite_destiny_path)
        getCoord = conn.execute("SELECT * FROM Coordinadores WHERE HASH =?", (hash,)).fetchone()
        conn.close()
        if getCoord:
            return redirect('loadings')

        # loadings_aprendiz
        conn = sql3.connect(Sqlite_destiny_path)
        getApren = conn.execute("SELECT * FROM loadings_aprendiz WHERE HASH =?", (hash,)).fetchone()
        conn.close()
        if getApren:
            request.session['getAprend'] = getApren
            ficha = getApren[8]

                # Verificar session de instructores
                
            if 'allInstructores' in request.session:
                
                if len(request.session['allInstructores']) == 0:
                    messages.error(request, f"Ya no hay mas Instructores para evaluar")
                    request.session.clear()
                    return redirect("home")
                else:
                    return redirect('pickInstructor')
            else:
                conn = sql3.connect(Sqlite_destiny_path)
                getInst = conn.execute("SELECT * FROM loadings_instructor WHERE FICHA =?", (ficha,)).fetchall()
                conn.close()
                for i in getInst:
                    if i not in allInstructores:
                        allInstructores.append(i)
                request.session['allInstructores'] = allInstructores
                return redirect('pickInstructor')

        # loadings_instructor
        conn = sql3.connect(Sqlite_destiny_path)
        getInst = conn.execute("SELECT * FROM loadings_instructor WHERE HASH =?", (hash,)).fetchone()
        conn.close()
        if getInst:
            request.session['instructorPicture'] = getInst
            # return redirect('upload_photo')
            return redirect('loadPicture')

        # No HASH
        messages.error(request, f'El HASH no se encuentra en la base de datos, por favor notifique a su instructor')
        return redirect('home')


def userLogout(request):
    request.session.flush()
    messages.success(request, "Has cerrado sesión.")
    logout(request)
    return redirect('home')


def loginPage(request):
    form = LogInForm()
    if request.method == 'POST':
        form = LogInForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('administracion')
        else:
            messages.error(request, f'Algo no salio bien, Intentalo de nuevo')
            return redirect('loginPage')

    context = {'title':'SENA - Iniciar Sesión', 'form':form}
    return render(request, 'evalinst/login.html', context)


def pickInstructor(request):
    getApren = request.session['getAprend']
    print(getApren)
    allInstructores = request.session['allInstructores']
    print(allInstructores)
    if len(allInstructores) == 0:
        messages.error(request, f"Ya no tienes instructores por evaluar, Gracias")
        request.session.clear()
        return redirect("home")
    else:
        context = {'title': "Eveluación Instructor", 'aprendix':getApren, 'instructores':allInstructores}
        return render(request, "evalinst/pickInst.html", context)


def testing(request):
    instructor = None

    if request.method == 'POST':
        instructor = request.POST.get('instructor')

    # Get Aprendiz
    getApren = request.session['getAprend']

    # Buscar instructor
    conn = sql3.connect(Sqlite_destiny_path)
    getInst = conn.execute("SELECT * FROM loadings_instructor WHERE NUMERO_DE_DOCUMENTO_INSTRUCTOR =?", (instructor,)).fetchone()
    conn.close()

    context = {'title': "Eveluación Instructor", 'instructor':getInst}
    return render(request, "evalinst/testing.html", context)

    #'aprendix':getApren,

def saveTest(request):
    timing = datetime.now().strftime("%b_%Y")
    if request.method == 'POST':
            # crear directorio si no existe
        endDir = crearTestingFolder()

        testing = pd.DataFrame([request.POST])
        instructoresMuchos = request.session['allInstructores']

        ficha = request.POST.get('ficha')
        instructor = request.POST.get('instructorid')
        aprendiz = request.POST.get('aprendizid')
        p01 = request.POST.get('p01')
        p02 = request.POST.get('p02')
        p03 = request.POST.get('p03')
        p04 = request.POST.get('p04')
        p05 = request.POST.get('p05')
        p06 = request.POST.get('p06')
        p07 = request.POST.get('p07')
        p08 = request.POST.get('p08')
        p09 = request.POST.get('p09')
        p10 = request.POST.get('p10')
        p11 = request.POST.get('p11')
        p12 = request.POST.get('p12')

            # Buscar instructor
        conn = sql3.connect(Sqlite_destiny_path)
        getInst = conn.execute("SELECT * FROM loadings_instructor WHERE NUMERO_DE_DOCUMENTO_INSTRUCTOR =?", (instructor,)).fetchone()
        conn.close()

        for i in instructoresMuchos:
            if i[3] == instructor:
                instructoresMuchos.remove(i)

        request.session['allInstructores'] = instructoresMuchos
        instructoresMuchos = request.session['allInstructores']

            # save to csv
        if "Testings_" + timing + ".csv" in os.listdir(endDir):
            testing.to_csv(endDir + "Testings_" + timing + ".csv", mode='a', index=False, header=False)
        else:
            testing.to_csv(endDir + "Testings_" + timing + ".csv", mode='a', index=False)

            # DATABASE
        conn = sql3.connect(Sqlite_destiny_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Testing (ficha,aprendizid,instructorid,p01,p02,p03,p04,p05,p06,p07,p08,p09,p10,p11,p12) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (ficha,aprendiz,instructor,p01,p02,p03,p04,p05,p06,p07,p08,p09,p10,p11,p12))
        conn.commit()
        conn.close()

        if len(instructoresMuchos) == 0:
            messages.error(request, f"Gracias por tu participación")
            return redirect("home")

    return redirect("pickInstructor")

"""
2a3cf90800623066d57c7a82a233264f    coordinacion

instruct
3e5dbe5cc0699069d8cae9a8b923d6b3    79169170
127dfa58b6577fb5839760e721ccd747    1023895786

aprendiz
4b5502f3e07f54a9fa8cd605be967748    2821670 
552239fa029dd459c2fb5a16fad7808a    2821670 

adf37fa3c0e680f84b2c4f9752519125
1dfcc70de70ea4d00aae8e43816f470c







# carga el archivo csv en la db
def insertAllData():
    conn=sql.connect("/home/gabriel/prog/analytics/csvSql/dbs/testdb.db")
    cursor=conn.cursor()
    csvData = readCsv()

    for row in csvData:
        Emp_ID = row[0]
        Name_Prefix = row[1]
        First_Name = row[2]
        Middle_Initial = row[3]
        Last_Name = row[4]
        Gender = row[5]
        Email = row[6]

        sqlQuery = f --->> usar tres comillas

        INSERT INTO hundred VALUES (
            '{Emp_ID}',
            '{Name_Prefix}',
            '{First_Name}',
            '{Middle_Initial}',
            '{Last_Name}',
            '{Gender}',
            '{Email}'
            )  --->> usar tres comillas
        cursor.execute(sqlQuery)
    conn.commit()
    conn.close()
"""
