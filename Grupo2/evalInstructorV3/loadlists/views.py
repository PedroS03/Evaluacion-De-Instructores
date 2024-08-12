import os
import hashlib
import pandas as pd
import sqlite3 as sql3
from datetime import datetime, date, timedelta
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from evalinstructor.utils import *
from dbs.dbs import *
from .mail import sendMailCoordinaciones

BASE_DIR = settings.BASE_DIR
timing = datetime.today().date()
dateEndCoordination = 15
dateEndPhoto = dateEndCoordination + 7
dateEndEvalua = dateEndCoordination + 7 + 15

def loadActivation(request):
    context = {"title": "Subir Archivo de Activación"}
    return render(request, "loadlists/loadActivation.html", context)


def activation(request):
    if request.method == "POST":
            # Get file and split for extension
        fileinn = request.FILES["instructorFileIn"]
        nameFile = fileinn.name
        filenamex = nameFile.split('.')
            # check if file is excel
        if filenamex[-1] == "xls" or filenamex[-1] == "xlsx":
            dataframe = pd.read_excel(fileinn, 'Coordinaciones') 
        else:
            messages.info(request, f'El archivo a precesar no es archivo excel, verifique que sea excel')
            return redirect('/')
            # Extraer info de las Coordinaciones
            # Delete first 2 rows from file
        dfcoord = dataframe.drop(dataframe.index[0:1])
        dfcoord.reset_index(drop=True, inplace=True)
        dfcoord.columns = dfcoord.iloc[0]
        dfcoord = dfcoord[1:8]
        dfcoord = clean_data_coordinacion(dfcoord)
        dfcoord = dfcoord.dropna()
            # create hash and assign group para Coordinaciones
        for i, row in dfcoord.iterrows():
            val = row['COORDINACION'] + row['NOMBRE_COORDINADOR'] + row['APELLIDOS_COORDINADOR'] + row['CORREO_COORDINADOR']
            dfcoord.at[i, 'HASH'] = hashlib.md5(val.encode()).hexdigest()
                # create Group
            dfcoord.at[i, 'GRUPO'] = "coordinador"
            centroFormacion = row['CENTRO_DE_FORMACION']
        dfcoord['FECHA_DE_UPLOAD'] = datetime.today().strftime('%m/%d/%Y %H:%M:%S')
            # Extract questions
        dfquestion = pd.read_excel(fileinn, 'Preguntas') 
        dfquestion = dfquestion.drop(dfquestion.index[0:1])
        dfquestion.reset_index(drop=True, inplace=True)
        dfquestion.columns = dfquestion.iloc[0]
        dfquestion = dfquestion[1:13]
        dfquestion = clean_data_pregunas(dfquestion)
            # Calculate dates
        startdateDf = dfcoord.at[1, 'FECHA_DE_COMIENZO']
        endCoordination = startdateDf + timedelta(days=dateEndCoordination)
        endInstPhoto = startdateDf + timedelta(days=dateEndPhoto)
        endEvaluation = startdateDf + timedelta(days=dateEndEvalua)
        times = {"STARTDATE": startdateDf,
                "ENDCOORDATE": endCoordination,
                "ENDPHOTODATE": endInstPhoto,
                "ENDEVALUACION": endEvaluation }
        evalDates = pd.DataFrame([times])
            # crear directorio si no existe
        endDir = createCoordinatorFolder()
            # save to Coordinaciones csv
        dfcoord.to_csv(endDir + "Coordinacion_" + centroFormacion + "_" + str(timing) + ".csv", index=False)
            # save to questions csv
        dfquestion.to_csv(endDir + "Preguntas_" + centroFormacion + "_"  + str(timing) + ".csv", index=False)
            # DATABASE Coordinaciones
        save_db(dfcoord, "Coordinadores")
            # DATABASE questions
        save_db(dfquestion, "Preguntas")
            # DATABASE Evaluacion
        save_db(evalDates, "EvalFechas")
            # Send Mail to Coordinations
        sendMailCoordinaciones()

    return redirect("administracion")


def loadings(request):
    sqlQuery = f"""SELECT * FROM Coordinadores"""
    coordinaciones = call_db(sqlQuery)
    if request.method == "POST":
        sqlQuery = f"""SELECT * FROM Coordinadores"""
        coordinaciones = call_db(sqlQuery)

    context = {'title': 'Subir Listas'}
    return render(request, 'loadlists/loadings.html', context)


def loadInstructores(request):
    if request.method == "POST":
            # Recibe file y separa nombre de la extension
        fileinn = request.FILES["instructorFileIn"]
        nameFile = fileinn.name
        filenamex = nameFile.split('.')
            # check if file is excel
        if filenamex[-1] == "xls" or filenamex[-1] == "xlsx":
            dataframe = pd.read_excel(fileinn) 
        else:
            messages.info(request, f'El archivo a precesar no es archivo excel, verifique que sea excel')
            return redirect('/')
            # Extract location info for Instructores
        REGION = dataframe.loc[0,:].values[7]
        CENTRO_DE_FORMACION = dataframe.loc[0,:].values[8]
            # Extract and Delete unused info from file
        dfinstructor = dataframe.drop(dataframe.index[0:2])
        dfinstructor.reset_index(drop=True, inplace=True)
        dfinstructor.columns = dfinstructor.iloc[0]
        dfinstructor = clean_data(dfinstructor)
        dfinstructor = dfinstructor.dropna()
        dfinstructor = dfinstructor.drop(0)
        dfinstructor.reset_index(drop=True, inplace=True)
            # create hash
        for i, row in dfinstructor.iterrows():
            val = row['NUMERO_DE_DOCUMENTO'] + row['NOMBRE'] + row['APELLIDOS']
            dfinstructor.at[i, 'HASH'] = hashlib.md5(val.encode()).hexdigest()
            # create extra info
        dfinstructor['GRUPO'] = 'instructor'
        dfinstructor['PHOTO'] = 'photo'
        dfinstructor['REGION'] = REGION
        dfinstructor['CENTRO_DE_FORMACION'] = CENTRO_DE_FORMACION
        dfinstructor['FECHA_DEL_REPORTE'] = datetime.now()
        dfinstructor.reset_index(drop=True, inplace=True)
            # create directorio si no existe
        endDir = crearInstructorFolder()
            # DATABASE instructores
        save_db(dfinstructor, "Instructores")
            # save to csv
        dfinstructor.to_csv(endDir + "instructores_" + str(timing) + ".csv", index=False)

    return redirect("home")


def loadAprendicesMany(request):
    aprendiz_origen_path = "/home/gabriel/Downloads/listados/"
    allApren = []
    # Load only xls, xlsx files
    for file in os.listdir(aprendiz_origen_path):
        if file.endswith('.xls') or file.endswith('.xlsx'):
            ficha1 = []
            ficha = ""
            lenficha = 6
            # Get ficha number
            data = pd.read_excel(io=aprendiz_origen_path + file, header=None)
            fechaReporte = data.iat[3,2]
            celx = data.iat[1,2]
            for i in celx:
                if lenficha >= 0:
                    ficha1.append(i)
                    lenficha -= 1
            ficha = ''.join(str(e) for e in ficha1)
            # Delete first 4 rows from file
            filenamex = file.split('.')
            dfx = pd.read_excel(io=aprendiz_origen_path + file, header=None)
            df1 = dfx.drop(dfx.index[0:4])
            df1.reset_index(drop=True, inplace=True)
            df1.drop(index=4)
            df1.columns = df1.iloc[0]
            df1 = df1[1:]
            # Add columns for fechaReporte and ficha
            df1['fecha_del_reporte'] = fechaReporte
            df1['ficha'] = ficha
            # Save processed sheets into one master dataframe
            allApren.append(df1)
        # Join all files in one dataframe
    dataframe = pd.concat(allApren, axis=0)
        # clean columns names and data
    dataframe = clean_data_aprendiz(dataframe)
        # create hash
    for i, row in dataframe.iterrows():
        val = row['NUMERO_DE_DOCUMENTO'] + row['NOMBRE'] + row['APELLIDOS']
        dataframe.at[i, 'HASH'] = hashlib.md5(val.encode()).hexdigest()
        # crear grupo
    dataframe['GRUPO'] = 'aprendiz'
        # DATABASE
    save_db(dataframe, "Aprendices")
        # Create directory if not exists
    endDir = crearAprendizFolder()
        # save to csv
    dataframe.to_csv(endDir + "aprendices_" + str(timing) + ".csv", index=False)

        # delete only xls, xlsx files
    for file in os.listdir(aprendiz_origen_path):
        if file.endswith('.xls') or file.endswith('.xlsx'):
            os.remove(aprendiz_origen_path + file)

    return redirect("home")


def uploadPhoto(request):
    if request.method == 'POST' and request.FILES['PHOTO']:
        myfile = request.FILES['PHOTO']
        numero_de_documento = request.POST.get('NUMERO_DE_DOCUMENTO')
        fs = FileSystemStorage()
        filename = fs.save(numero_de_documento, myfile)
        uploaded_file_url = fs.url(filename)
        sqlQuery = f"""UPDATE Instructores SET PHOTO = ? WHERE NUMERO_DE_DOCUMENTO =?"""
        update_db(sqlQuery, uploaded_file_url, numero_de_documento)

        context = {'uploaded_file_url': uploaded_file_url}
        return render(request, 'loadlists/instructor.html', context)

    context = {'title': "Load Foto"}
    return render(request, 'loadlists/uploadPhoto.html', context)


def instructorx(request):
    if request.method == 'POST':
        doxx = request.POST.get('documento')

        context = {'title': "instructor", 'doxx': doxx}
        return render(request, 'loadlists/instructorx.html', context)

    context = {'title': "instructor"}
    return render(request, 'loadlists/instructorx.html', context)
