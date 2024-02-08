# IOT_ultrasonic_presence_sensor


## Description

* Ultrasonic-Sensor transmitting presence to an MQTT Server.
* Additional you can use MQTT->Telegraf->InfluxDB->Grafana for Visualization.
* Housing for Ultrasonic-Sensor and ESP32 for easy installation on every surface.

The microcontroller send the distance to the MQTT Server and you can choose in the software, from when presence is true.


## Hardware

* ESP32
* Ultrasonic-Sensor HC-SR04
* Cable
* Power supply for ESP32 and Ultrasonic-Sensor 


## First steps

* Print the housing
* Adapt your SSID for internet connection and the adress for the MQTT server in the microcontroller files.
* Connect the sensor to the microcontroller using pins. -> Conifigure those pins in the software
* Copy the software on the microcontroller.
* Enjoy

