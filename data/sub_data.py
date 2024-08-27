import paho.mqtt.client as mqtt
from random import randrange, uniform
import time, json
from datetime import datetime
import psycopg2 as pg

# Connect to the Database
conn = pg.connect("host=localhost dbname=postgres user=postgres password='Jelibi20'")
try:
    cur = conn.cursor()
    print("Connection to the DB established")
except (Exception, pg.DatabaseError) as error:
    print(error)


# MQTT Setup
port = 1883
# mqttBroker = 'broker.hivemq.com'
mqttBroker = 'test.mosquitto.org' # For Raspberry Pi
client = mqtt.Client()
# topic = "Jay/m1/sensorData" 
topic = "jay/machine1/sensorData" # For Raspberry Pi

def on_connect(client, userdata, flags, rc):
    print(f"Connected to Broker with result code {rc}")
    if rc!=0:
        print("Connection to Broker not established...Something is wrong..")
    client.subscribe(topic)


def on_log(client, userdata, level, buffer):
    print("Log: ", buffer)

def on_message(client, userdata, message):
    if message.topic == topic:
        msg = message.payload.decode('utf-8')
        dataObj = json.loads(msg)
    
    now = datetime.now()

    dateSTR = now.strftime('%Y%m%d%H%M%S')
    sequence = int(dateSTR)

    insertCMD = """ INSERT INTO public."factorymachines" VALUES(%s,%s,%s,%s,%s,%s,%s) """
    values = (dataObj['sentDate'], dataObj['temperature'], dataObj['pressure'], dataObj['status'], dataObj['humidity'], sequence, dataObj['machine_id'])

    try:
        cur.execute(insertCMD, values)
        conn.commit()
        print("DB transaction executed")
    except (Exception, pg.DatabaseError) as error:
        print(error)


def on_disconnect(client, userdata, rc=0):
    client.loop_stop()

# Connect to the broker
client.connect(mqttBroker, port, 60)
client.on_log = on_log
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
time.sleep(3)
client.loop_forever()