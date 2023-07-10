import sys
from Adafruit_IO import MQTTClient
import random as r
import time
import requests

from account import AIO_USERNAME, AIO_KEY

EQUATION_API = "https://io.adafruit.com/api/v2/tinvietle/feeds/equation"
global_equation = ""

def message(client , feed_id , payload):
    global global_equation
    print(f"Received payload from \"{feed_id}\": {payload}")
    if (feed_id == "equation"):
        global_equation = payload

def init_global_equation():
    global global_equation
    headers = {}
    x = requests.get(url = EQUATION_API, headers = headers, verify = False)
    x = x.json()
    global_equation = x["last_value"]
    print(f"Latest equation value: {global_equation}")

def calculate(x1, x2, x3):
    result = eval(global_equation)
    print(f"Resut from Adafruit {global_equation}: {result}")
    return result

client = MQTTClient(AIO_USERNAME , AIO_KEY)

client.connect()
client.loop_background()
init_global_equation()

while True:
    temp_value = r.randint(20, 50)
    humi_value = r.randint(0, 100)
    soil_value = r.randint(0, 100)
    water_value = r.randint(0,100)
    client.publish("temperature", temp_value)
    time.sleep(2)
    client.publish("humidity", humi_value)
    time.sleep(2)
    client.publish("soil_moisture", soil_value)
    time.sleep(2)
    client.publish("water_level", water_value)
    time.sleep(2)
    if ( 20 <calculate(temp_value, humi_value, soil_value)/ 3) < 60:
        client.publish("light_switch", "ON")
    else:
        client.publish("light_switch", "OFF")
    time.sleep(2)
    if water_value <= 10: 
        client.publish("pump_switch", "ON")
    else:
        client.publish("pump_switch", "OFF")
    time.sleep(2)
    if (soil_value > 90):
        client.publish("message", "Don't water the tree")
    elif (80 < soil_value <= 90):
        client.publish("message","Watering 10 minute")
    elif (70 < soil_value <= 80):
        client.publish("message","Watering 15 minute")
    elif (soil_value <= 70):
        client.publish("message","Watering 20 minute")
    time.sleep(4)
    # client.publish("plot_result", calculate(sensor1_value, sensor2_value, sensor3_value))
    # time.sleep(2)
