import psycopg2 as pg
import pandas as pd
import json
import requests

def connectDB():
    conn = pg.connect("host=localhost dbname=postgres user=postgres password='Jelibi20'")
    try:
        print("Connection Established")
        cur = conn.cursor()
    except (Exception, pg.DatabaseError) as error:
        print(error)
    
    return conn, cur

def getData(conn, cur):
    try:
        cmd = """ SELECT * FROM public.factorymachines ORDER BY sequence DESC LIMIT 1"""
        cur.execute(cmd)
        df = pd.read_sql_query(cmd, conn)
        return df

    except (Exception, pg.DatabaseError) as error:
        print(error)

#----------------BELOW CODE IS FOR RESTFUL SERVER FUNCTIONS-------------
def getSensorDataOne2(id):
    resp = requests.get("http://127.0.0.1:3000/lastOne?machineID="+str(id))
    if resp.status_code == 200:

        records = json.loads(resp.content)
        df = pd.read_json(records)
    return df

def getSensorDataOne():
    resp = requests.get("http://127.0.0.1:3000/lastOne")
    if resp.status_code == 200:

        records = json.loads(resp.content) 
        df = pd.read_json(records)
    return df

