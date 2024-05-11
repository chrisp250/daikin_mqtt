      import time
import paho.mqtt.client as mqtt
import configparser
import daikin

#Configuration file reader
config = configparser.ConfigParser()
config.read("daikin.ini")

mqtt_server=config['mqtt']['server']
mqtt_port=int(config['mqtt']['port'])
mqqt_username = config['mqtt']['username']
mqqt_password = config['mqtt']['password']
base_topic = config['mqtt']['base_topic']
ac_address = config['unit']['ip']

#Define Daikin class
aircon = daikin.Daikin(ac_address)

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
    if message.topic == (base_topic+'/modecommand'): #Is it a mode change message
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
    elif message.topic == (base_topic+'/temperaturecommand'): #Is it a temperature change message
        print ("Set temperature:",str(message.payload.decode("utf-8")))
        aircon.set_temp(message.payload.decode("utf-8"))
#    update_request()

#Request an update on AC status
def update_request():
    while not aircon.get_status():
        time.sleep(30) #Wait if can't connect to AC unit and retry
    #print("Polling...")
    # Why use msg.encode('utf-8') here
    # MQTT is a binary based protocol where the control elements are binary bytes and not text strings.
    # Topic names, Client ID, Usernames and Passwords are encoded as stream of bytes using UTF-8.
    msg = aircon.mode
    info = mqttClient.publish(
        topic=base_topic+'/mode',
        payload=msg.encode('utf-8'),
        qos=0,
    )
    info = mqttClient.publish(
        topic=base_topic+'/temperature',
        payload=aircon.temperature,
        qos=0,
    )
    info = mqttClient.publish(
        topic=base_topic+'/temperaturesp',
        payload=aircon.temperaturesp,
        qos=0,
    )
    info = mqttClient.publish(
        topic=base_topic+'/humidity',
        payload=aircon.humidity,
        qos=0,
    )
    info = mqttClient.publish(
        topic=base_topic+'/fanmode',
        payload=aircon.fanmode,
        qos=0,
    )
    # Because published() is not synchronous,
    # it returns false while he is not aware of delivery that's why calling wait_for_publish() is mandatory.
    info.wait_for_publish()
    #print(info.is_published())


mqttClient = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "daikin_studio")
mqttClient.on_publish = on_publish
mqttClient.on_message = on_message
mqttClient.on_subscribe = on_subscribe
mqttClient.username_pw_set(mqqt_username, mqqt_password)
mqttClient.connect(mqtt_server, mqtt_port)

mqttClient.subscribe(base_topic+'/modecommand')
mqttClient.subscribe(base_topic+'/temperaturecommand')
# start a new thread
mqttClient.loop_start()

while True:
    update_request()
    time.sleep(30)
