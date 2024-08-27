import paho.mqtt.client as mqtt
from random import randrange, uniform
import time, json
from datetime import datetime

# MQTT Setup
port = 1883
mqttBroker = 'broker.hivemq.com'
client = mqtt.Client()
topic = "Jay/m1/sensorData" 

def on_log(client, userdata, level, buffer):
    print("Log: ", buffer)

# Connect to the broker
client.connect(mqttBroker, port, 60)
client.on_log = on_log

dataObj = {}
counter = 0

while True:
    T = round(uniform(10.0, 50.0), 2)
    P = randrange(50, 100)
    H = randrange(10, 100)
    now = datetime.now()

    dataObj['machine_id'] = 200
    dataObj['sentDate'] = str(now)
    dataObj['temperature'] = T
    dataObj['pressure'] = P
    dataObj['humidity'] = H

    counter+=1

    if counter % 30 == 0:
        dataObj['status'] = "OFF"

        jsonData = json.dumps(dataObj)
        client.publish(topic, jsonData, qos=0)
        print("JSON Data Sent", dataObj)
        time.sleep(10)
    
    else:
        dataObj['status'] = "ON"
        jsonData = json.dumps(dataObj)
        client.publish(topic, jsonData, qos=0)
        print("JSON Data Sent", dataObj)
        time.sleep(3)


