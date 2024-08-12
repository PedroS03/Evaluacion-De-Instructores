import os
import sqlite3 as sql3
from django.conf import settings

BASE_DIR = settings.BASE_DIR


def save_db(dataframe, table):
    conn = sql3.connect(os.path.join(BASE_DIR, "dbs/staff.db"))
    dataframe.to_sql(name=table, con=conn, if_exists="replace", index=False)
    conn.close()


def call_db(sqlQuery):
    conn = sql3.connect(os.path.join(BASE_DIR, "dbs/staff.db"))
    dbData = conn.execute(sqlQuery,).fetchall()
    conn.close()

    return dbData


def call_db_one(sqlQuery, adition):
    conn = sql3.connect(os.path.join(BASE_DIR, "dbs/staff.db"))
    dbData = conn.execute(sqlQuery, (adition,)).fetchone()
    conn.close()

    return dbData


def update_db(sqlQuery, data1, data2):
    conn = sql3.connect(os.path.join(BASE_DIR, "dbs/staff.db"))
    cur = conn.cursor()
    cur.execute(sqlQuery, (data1, data2))
    conn.commit()
    conn.close()

