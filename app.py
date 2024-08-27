from flask import Flask, request
from flask_restful import Resource, Api
from flask import jsonify

import psycopg2 as pg
import pandas as pd

# Connect to the DB

conn = pg.connect(host='localhost', dbname='postgres', user='postgres', password='Jelibi20')
try:
    print("Connection Established")
    cur = conn.cursor()
except (Exception, pg.DatabaseError) as error:
    print(error)

app = Flask(__name__)
api = Api(app)

class Machines(Resource):
    def get (self):
        try:
            cmd = 'SELECT * FROM public.factorymachines'
            cur.execute(cmd)
            records = cur.fetchall()

            return jsonify({'machineList': [rec for rec in records]})
        
        except(Exception, pg.DatabaseError) as error:
            print(error)

class MachinesDataOne(Resource):
    def get(self):
        try:
            cmd = 'SELECT * FROM public.factorymachines ORDER BY sequence DESC LIMIT 1'
            cur.execute(cmd)
            df = pd.read_sql_query(cmd, conn)
            return df.to_json()
        
        except (Exception, pg.DatabaseError) as error:
            print(error)


# Here we enlist all the available resources
api.add_resource(Machines, '/machinelist')
api.add_resource(MachinesDataOne, '/lastOne')

if __name__=='__main__':
    app.run(port=3000, debug=False)

