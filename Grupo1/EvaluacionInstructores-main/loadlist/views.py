import os
import json
import hashlib
import sqlite3 as sql3
import pandas as pd
from PIL import Image
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from datetime import datetime
from .models import Instructor, Aprendiz, Evaluacion, Coordinador
from .utils import *
from .toHash import toHash, toHashCoord
from django.utils.timezone import now
from administracion.decorators import EstablecerFechas
from .sendEmail import *


now = datetime.now()
year = now.strftime("%Y")

# aprendiz_origen_path = "C:/Users/USUARIO/Desktop/PruebasLista/"
aprendiz_origen_path = "D:/Users/Aprendiz/Desktop/PruebasLista/"
# Folder to sqlite3
Sqlite_destiny_path = "dbs/staff.db"
# to save csvs 
Aprendice_destiny_path = "csvs/laprend/"
instructor_destiny_path = "csvs/linst/"
coordinador_destiny_path = "csvs/lcoord/"


@EstablecerFechas
def loadings(request):
    context = {'title': 'Subir Listas'}
    return render(request, 'loadlist/loadings.html', context)


def loadAprendicesMany(request):
    timing = datetime.now().strftime("%b_%Y")
    frames=[]
    xls_files = []
    allApren = []

    # Create directory if not exists
    endDir = crearAprendizFolder()

    # Load only xls, xlsx files
    for file in os.listdir(aprendiz_origen_path):
        if file.endswith('.xls') or file.endswith('.xlsx'):
            ficha1 = []
            ficha = ""
            lenficha = 6

            # Get ficha number
            data = pd.read_excel(io=aprendiz_origen_path + file, header=None)
            fechaReporte = data.iat[3,2]
            celx = data.iat[1,3]
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
        

        # enviar los correos
        for i, row in dataframe.iterrows():
            context = ({"ficha": row['FICHA'], "first_name": row['NOMBRE'], 'last_name': row['APELLIDOS'], 'hash': row['HASH']})
            emailSubject = "Jornada de evaluacion de tus Instructores"
            sendTo = row['CORREO_ELECTRONICO']

    #        sendEmail(request, context, emailSubject, sendTo)
            dataframe.at[i, 'HASH_SEND'] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        # crear grupo
    dataframe['GRUPO'] = 'aprendiz'

    messages.success(request,'Se subió correctamente la plantilla de los aprendices')

        # DATABASE
    conn = sql3.connect(Sqlite_destiny_path)
    dataframe.to_sql(name="loadings_aprendiz", con=conn, if_exists="append", index=False)
    conn.close()
        # save to csv
    dataframe.to_csv(endDir + "allAprendiz.csv", index=True)

        # delete only xls, xlsx files
    for file in os.listdir(aprendiz_origen_path):
        if file.endswith('.xls') or file.endswith('.xlsx'):
            os.remove(aprendiz_origen_path + file)

    return redirect("loadings")


def loadInstructores(request):
    timing = datetime.now().strftime("%b_%Y")
    if request.method == "POST":
            # crear directorio si no existe
        endDir = crearInstructorFolder()
            # Recibe file y separa nombre de la extension
        fileinn = request.FILES["instructorFileIn"]
        nameFile = fileinn.name
        filenamex = nameFile.split('.')

        if filenamex[1] == "xls" or filenamex[1] == "xlsx":
            dataframe = pd.read_excel(fileinn)
        else:
            messages("El archivo no es valido, revise que sea .xls o .xlsx")
            return redirect("/")
        
            # Limpia la data
        dataframe = clean_data_instructor(dataframe)
            # create hash
        for i, row in dataframe.iterrows():
            val = row['NUMERO_DE_DOCUMENTO_INSTRUCTOR'] + row['NOMBRE'] + row['APELLIDOS']
            dataframe.at[i, 'HASH'] = hashlib.md5(val.encode()).hexdigest()

            # crear grupo
        dataframe['GRUPO'] = 'instructor'
        dataframe['PICTURE'] = 'media/default.png'
        dataframe['FECHA_DEL_REPORTE'] = datetime.now()
        messages.success(request,'Se subió correctamente la plantilla de los instructores')
            # DATABASE
        conn = sql3.connect(Sqlite_destiny_path)
        dataframe.to_sql(name="loadings_instructor", con=conn, if_exists="append", index=False)
        conn.close()
            # save to csv
        dataframe.to_csv(endDir + "allInstructores" + timing + ".csv", index=True)

    return redirect("loadings")


def loadPicture(request):
    instructorPicture = request.session['instructorPicture']
    ccInstructor =  instructorPicture[3]

    if request.method == "POST":
        picture = request.FILES["picture"]
        namePicture = picture.name
        filenamex = namePicture.split('.')

        if filenamex[0] == ccInstructor:
            fileSistem = FileSystemStorage()
            filename = fileSistem.save(picture.name, picture)
            PICTURE = fileSistem.url(filename)
            print(PICTURE)
            conn = sql3.connect(Sqlite_destiny_path)
            cur=conn.cursor()
            print(ccInstructor)
            #sql="UPDATE loadings_instructor SET PICTURE = '"+PICTURE+"' WHERE NUMERO_DE_DOCUMENTO_INSTRUCTOR ="+ccInstructor
            sql = "UPDATE loadings_instructor SET PICTURE = ? WHERE NUMERO_DE_DOCUMENTO_INSTRUCTOR = ?"
            # cursor.execute("UPDATE loadings_instructor SET PICTURE = ? WHERE NUMERO_DE_DOCUMENTO_INSTRUCTOR = ?")
            cur.execute(sql, (PICTURE, ccInstructor))
            conn.commit()
            conn.close()

            messages.success(request,'Se subió correctamente la fotografia del Instructor')
            return redirect("loadPicture")

        else:
            messages.success(request,'La fotografia debe llamarse con el numero de documento del instructor, ej: 00000000.jpg')
            return redirect("loadPicture")
        
    context = {'title': 'Subir Foto Instructor', 'instructor':instructorPicture}
    return render(request, 'loadlist/loadPicture.html', context)


def loadCoordinaciones(request):
    timing = datetime.now().strftime("%b_%Y")

    if request.method == "POST":
            # crear directorio si no existe
        endDir = crearCoordinadorFolder()
        
            # Recibe file y separa nombre de la extension
        fileinn = request.FILES["activacionFileIn"]
        nameFile = fileinn.name
        filenamex = nameFile.split('.')

        if filenamex[1] == "xls" or filenamex[1] == "xlsx":
            dataframe = pd.read_excel(fileinn)
        else:
            messages.warning("El archivo no es valido, revise que sea .xls o .xlsx")
            return redirect("/")

            # Extraer info de la Evaluacion
        dfeval = pd.DataFrame({"REGIONAL": [dataframe.iat[2,0]],
                            "CENTRO": [dataframe.iat[2,1]],
                            "FECHA_LISTAS": [dataframe.iat[2,2]],
                            "FECHA_EVALUACION": [dataframe.iat[2,3]],
                            "FECHA_DE_SOLICITUD": [datetime.today().strftime('%Y-%m-%d %H:%M:%S')] })
        
            # DATABASE Evaluacion
        conn = sql3.connect(Sqlite_destiny_path)
        dfeval.to_sql(name="Evaluacion", con=conn, if_exists="append", index=False)
        conn.close()

            # save to Evaluaciones csv
        dfeval.to_csv(endDir + "Evaluaciones_" + timing + ".csv", index=False)

            # Extraer info de las Coordinaciones
            # Delete first 6 rows from file
        dfcoord = dataframe.drop(dataframe.index[0:5])
        dfcoord.reset_index(drop=True, inplace=True)
        #df1.drop(index=4)
        dfcoord.columns = dfcoord.iloc[0]
        dfcoord = dfcoord[1:]

            # create hash para Coordinaciones
        for i, row in dfcoord.iterrows():
            val = row['COORDINACION'] + row['NOMBRE'] + row['APELLIDOS'] + row['EMAIL']
            dfcoord.at[i, 'HASH'] = hashlib.md5(val.encode()).hexdigest()

            # create Grupo
        dfcoord.at[i, 'GRUPO'] = "coordinador"

        dfcoord['REGIONAL'] = dataframe.iat[2,0]
        dfcoord['CENTRO'] = dataframe.iat[2,1]
        dfcoord['FECHA_LISTAS'] = dataframe.iat[2,2]
        dfcoord['FECHA_DE_UPLOAD'] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

            # enviar los correos
        for i, row in dfcoord.iterrows():
            context = ({"regional": row['REGIONAL'],"centro": row['CENTRO'],"coordinacion": row['COORDINACION'], "first_name": row['NOMBRE'], 'last_name': row['APELLIDOS'],'fecha_listas': row['FECHA_LISTAS'], 'hash': row['HASH']})
            emailSubject = "Jornada de evaluacion de tus Instructores"
            sendTo = row['EMAIL']

    #        sendEmailCoord(request, context, emailSubject, sendTo)
            dataframe.at[i, 'HASH_SEND'] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
            
        messages.success(request,'Se enviaron correctamente los correos')

            # DATABASE Coordinaciones
        conn = sql3.connect(Sqlite_destiny_path)
        dfcoord.to_sql(name="Coordinadores", con=conn, if_exists="append", index=False)
        conn.close()

            # save to Coordinaciones csv
        dfcoord.to_csv(endDir + "Coordinadores" + timing + ".csv", index=False)

    return redirect("administracion")


"""
2a3cf90800623066d57c7a82a233264f      coordinacion

instruct
3e5dbe5cc0699069d8cae9a8b923d6b3    79169170
127dfa58b6577fb5839760e721ccd747    1023895786

"""

