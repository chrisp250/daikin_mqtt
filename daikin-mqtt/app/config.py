import yaml
import os
import sys
import json

# Configuration file reader
# Env variables can be used to override the config file settings
# Example:
# export DAIKIN_MQTT_CONFIG_GENERAL=""
# export DAIKIN_MQTT_CONFIG_MQTT_SERVER="localhost"
# export DAIKIN_MQTT_CONFIG_MQTT_PORT=1883
# export DAIKIN_MQTT_CONFIG_MQTT_USERNAME="mqtt_username"
# export DAIKIN_MQTT_CONFIG_MQTT_PASSWORD="mqtt_password"
# export DAIKIN_MQTT_CONFIG_UNITS='[{"name": "unit_name", "address": "unit_address"}]'

class Config:
    def __init__(self):
        if "CONFIG_PATH" in os.environ:
            self.configPath = os.environ['CONFIG_PATH']
        else:
            self.configPath = "daikin.yaml"

    def getConfig(self):
        valid_json = True
        valid_yaml = True

        with open(self.configPath) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

        if "DAIKIN_MQTT_CONFIG_GENERAL" in os.environ:
            general = os.environ["DAIKIN_MQTT_CONFIG_GENERAL"]
        else:
            general = config['general']

        if "DAIKIN_MQTT_CONFIG_MQTT_SERVER" in os.environ:
            mqtt_server = os.environ["DAIKIN_MQTT_CONFIG_MQTT_SERVER"]
        else:
            mqtt_server = config['mqtt']['server']

        if "DAIKIN_MQTT_CONFIG_MQTT_PORT" in os.environ:
            mqtt_port = int(os.environ["DAIKIN_MQTT_CONFIG_MQTT_PORT"])
        else:
            mqtt_port = config['mqtt']['port']

        if "DAIKIN_MQTT_CONFIG_MQTT_USERNAME" in os.environ:
            mqtt_username = os.environ["DAIKIN_MQTT_CONFIG_MQTT_USERNAME"]
        else:
            mqtt_username = config['mqtt']['username']

        if "DAIKIN_MQTT_CONFIG_MQTT_PASSWORD" in os.environ:
            mqtt_password = os.environ["DAIKIN_MQTT_CONFIG_MQTT_PASSWORD"]
        else:
            mqtt_password = config['mqtt']['password']

        if "DAIKIN_MQTT_CONFIG_UNITS" in os.environ:
            try:
                units = json.loads(os.environ["DAIKIN_MQTT_CONFIG_UNITS"])
            except:
                valid_json = False

            try:
                units = yaml.load(os.environ["DAIKIN_MQTT_CONFIG_UNITS"])
            except:
                valid_yaml = False

            if not valid_json and not valid_yaml:
                units = config['units']
        else:
            units = config['units']


        if units[0]["name"] is None or units[0]["address"] is None:
            print("Unit name or address is not set in config file")
            sys.exit(1)

        return {
            "general": general,
            "mqtt" : {
                "server": mqtt_server,
                "port": mqtt_port,
                "username": mqtt_username,
                "password": mqtt_password
            },
            "units": units
        }
