# This code is only to be implemented on Raspberry Pi

import paho.mqtt.client as mqtt
import time
import json
from sense_hat import SenseHat

# MQTT Setup
port = 1883
mqttBroker = 'test.mosquitto.org'
client = mqtt.Client()
sense = SenseHat()

def on_log(client, userdata, level, buffer):
    print("Log: ", buffer)

# Connect to the MQTT broker
client.connect(mqttBroker, port, 60)

# Call back function
client.on_log = on_log

# Set up variables
dataObj = {}
counter = 0
red = (255, 0, 0)
orange = (255, 165, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
purple = (160, 32, 240)
white = (255, 255, 255)

sense.clear(white)
time.sleep(1)
sense.show_message("Hello World!")