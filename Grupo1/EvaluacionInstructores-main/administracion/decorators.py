from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from .views import error403
import sqlite3 as sql3

Sqlite_destiny_path = "..\EvaluacionInstructores\dbs\staff.db"


def EstablecerFechas(view_func):

    def wrapper(request, *args, **kwargs):
        try:
            sqlQuery = f"""SELECT * FROM Evaluacion"""
            conn = sql3.connect(Sqlite_destiny_path)
            activaciones = conn.execute(sqlQuery,).fetchall()
            conn.close()
            td = timedelta(15)
            print(activaciones)
            # Verificar si la fecha actual está dentro del rango permitido
            start_date_listas = datetime.strptime(activaciones[0][2], '%Y-%m-%d %H:%M:%S' ) # Fecha de inicio permitida
            print(start_date_listas)
            end_date_listas = start_date_listas + td   # Fecha de fin permitida
            print(end_date_listas)
            current_date = datetime.now()
            if not (start_date_listas <= current_date <= end_date_listas):
                return redirect(error403)
            # Si la fecha actual está dentro del rango permitido, continuar con la vista original
            return view_func(request, *args, **kwargs)
        except:
            return redirect(error403)
    return wrapper