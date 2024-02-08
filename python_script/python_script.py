import time
import json
import paho.mqtt.client as mqtt

last_distance = 0
last_change_time = 0
anwesenheit = False
# Werte für cooldown & max_req_dist können noch optimiert werden
cooldown = 5
max_req_dist = 100

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("homie/ESP32_Studentenlabor_1/distance")

def on_message(client, userdata, msg):
    global last_distance, last_change_time, anwesenheit
    payload = json.loads(msg.payload.decode())
    distance = float(payload)
    #print("Received distance:", distance)
    if last_distance is None:
        last_distance = distance
    else:
        if abs(distance - last_distance) > 10 and distance < max_req_dist:
            anwesenheit = True
            last_change_time = time.time()
        elif last_change_time is not None and time.time() - last_change_time > cooldown:
            anwesenheit = False
        last_distance = distance
    if anwesenheit == True:
        print("besetzt")
    else:
        print("nicht besetzt")

client = mqtt.Client()
client.username_pw_set("bobm", password="letmein")
client.on_connect = on_connect
client.on_message = on_message

client.connect("158.180.44.197", 1883, 60)

client.loop_forever()

