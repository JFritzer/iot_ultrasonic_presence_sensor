from django.http import HttpResponse
from django.template import loader
import time
import json
import paho.mqtt.client as mqtt
import plotly.graph_objs as go
import threading

def displaymqtt(request):
    global distance_data, anwesenheit
    template = loader.get_template('page.html')
    # Extract data for Plotly chart
    x_data = list(range(len(distance_data)))
    y_data = distance_data
    # Create a Plotly trace for the distance data
    trace = go.Scatter(
        x=x_data,
        y=y_data,
        mode='lines+markers',
        name='Distance (cm)'
    )
    # Create layout for the plot
    layout = go.Layout(
        title='Distance over Time',
        xaxis=dict(title='Time'),
        yaxis=dict(title='Distance (cm)')
    )
    # Plot the chart
    plot_div = go.Figure(data=[trace], layout=layout).to_html(full_html=False)
    # Pass plot_div and presence status to the template
    context = {
        'plot_div': plot_div,
        'anwesenheit': anwesenheit
    }
    return HttpResponse(template.render(context, request))
    #template = loader.get_template('page.html')
    #return HttpResponse(template.render())


last_distance = 0
last_change_time = 0
anwesenheit = False
# Werte für cooldown & max_req_dist können noch optimiert werden
cooldown = 5
max_req_dist = 100
distance_data = []

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("homie/ESP32_Studentenlabor_1/distance")

def on_message(client, userdata, msg):
    global last_distance, last_change_time, anwesenheit
    payload = json.loads(msg.payload.decode())
    distance = float(payload)
    distance_data.append(distance)
    if len(distance_data) > 50:
        distance_data.pop(0)
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
    #if anwesenheit == True:
    #    print("besetzt")
    #else:
    #    print("nicht besetzt")

def mqtt_loop():
    client = mqtt.Client()
    client.username_pw_set("bobm", password="letmein")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("158.180.44.197", 1883, 60)
    client.loop_forever()

mqtt_thread = threading.Thread(target=mqtt_loop)
mqtt_thread.start()
