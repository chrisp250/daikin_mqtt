import time
import re

import paho.mqtt.client as mqtt
import yaml
import daikin
import config
import os
import sys

# Check CONFIG_PATH environment variable

print("Starting Daikin MQTT")

#Configuration file reader
config = config.Config().getConfig()

print("Loaded configuration:", config)

#Publish succeeded
def on_publish(client, userdata, mid, reason_code, properties):
    #    print("sent a message")
    exit

# Subscribed to a new topic
def on_subscribe(client, userdata, mid, reason_code_list, properties):
    # Since we subscribed only for a single channel, reason_code_list contains
    # a single entry
    if reason_code_list[0].is_failure:
        #print(f"Broker rejected you subscription: {reason_code_list[0]}")
        exit
    else:
        #print(f"Broker granted the following QoS: {reason_code_list[0].value}")
        exit

#Message received
def on_message(client, userdata, message):
    #print("Topic:", message.topic," Payload:",message.payload)
    if "modecommand" in message.topic:
        print ("Set mode:",str(message.payload.decode("utf-8")))
        match str(message.payload.decode("utf-8")):
            case "cool":
                aircon.switch_mode("cool")
            case "dry":
                aircon.switch_mode("dry")
            case "heat":
                aircon.switch_mode("heat")
            case "fan_only":
                aircon.switch_mode("fan_only")
            case "auto":
                aircon.switch_mode("auto")
            case "off":
                aircon.switch_mode("off")
    elif "temperaturecommand" in message.topic: #Is it a temperature change message
        print ("Set temperature:",str(message.payload.decode("utf-8")))
        aircon.set_temp(message.payload.decode("utf-8"))
#    update_request()

#Request an update on AC status
def update_request(aircon, topic):
    while not aircon.get_status():
        time.sleep(30) #Wait if can't connect to AC unit and retry
    #print("Polling...")
    # Why use msg.encode('utf-8') here
    # MQTT is a binary based protocol where the control elements are binary bytes and not text strings.
    # Topic names, Client ID, Usernames and Passwords are encoded as stream of bytes using UTF-8.
    msg = aircon.mode
    info = mqttClient.publish(
        topic=topic+'/mode',
        payload=msg.encode('utf-8'),
        qos=0,
    )
    info = mqttClient.publish(
        topic=topic+'/temperature',
        payload=aircon.temperature,
        qos=0,
    )
    info = mqttClient.publish(
        topic=topic+'/temperaturesp',
        payload=aircon.temperaturesp,
        qos=0,
    )
    info = mqttClient.publish(
        topic=topic+'/humidity',
        payload=aircon.humidity,
        qos=0,
    )
    info = mqttClient.publish(
        topic=topic+'/fanmode',
        payload=aircon.fanmode,
        qos=0,
    )
    # Because published() is not synchronous,
    # it returns false while he is not aware of delivery that's why calling wait_for_publish() is mandatory.
    info.wait_for_publish()
    #print(info.is_published())



#Air conditioners and topics
aircons = list()
topics = list()

# Initialize mqttClient
mqttClient = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "daikin_mqtt")
mqttClient.on_publish = on_publish
mqttClient.on_message = on_message
mqttClient.on_subscribe = on_subscribe

if config["mqtt"]["username"] is not None and config["mqtt"]["password"] is not None:
    mqttClient.username_pw_set(config["mqtt"]["username"], config["mqtt"]["password"])

try:
    mqttClient.connect(config["mqtt"]["server"], config["mqtt"]["port"])
except TimeoutError:
    print("Connection to MQTT broker timed out")


# Subscribe to topics and Daikin client
for unit in config["units"]:
    mqttClient.subscribe("climate" + "/" + unit["name"] + "/" + "modecommand")
    mqttClient.subscribe("climate" + "/" + unit["name"] + "/" +'/temperaturecommand')

    aircons.append(daikin.Daikin(unit["address"]))
    topics.append("climate" + "/" + unit["name"])

# start a new thread
mqttClient.loop_start()

while True:
    for aircon in aircons:
        update_request(aircon, topics[aircons.index(aircon)])

    time.sleep(30)
