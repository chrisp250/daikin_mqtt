import time
import paho.mqtt.client as mqtt
import configparser
import daikin

#Configuration file reader
config = configparser.ConfigParser()
config.read("daikin.ini")

mqtt_server=config['mqtt']['server']
mqtt_port=int(config['mqtt']['port'])
base_topic = config['mqtt']['base_topic']
ac_address = config['unit']['ip']

#Define Daikin class
aircon = daikin.Daikin(ac_address)

#def on_publish(client, userdata, mid):
def on_publish(client, userdata, mid, reason_code, properties):
#    print("sent a message")
    exit


mqttClient = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "daikin_studio")
mqttClient.on_publish = on_publish
mqttClient.connect(mqtt_server, mqtt_port)
# start a new thread
mqttClient.loop_start()

# Why use msg.encode('utf-8') here
# MQTT is a binary based protocol where the control elements are binary bytes and not text strings.
# Topic names, Client ID, Usernames and Passwords are encoded as stream of bytes using UTF-8.
while True:
    aircon.get_status()
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


    # Because published() is not synchronous,
    # it returns false while he is not aware of delivery that's why calling wait_for_publish() is mandatory.
    info.wait_for_publish()
    #print(info.is_published())
    
    time.sleep(60)
