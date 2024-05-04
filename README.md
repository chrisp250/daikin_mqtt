# MQTT integration for Daikin airconditoners
I developed this integration to get my AC to work again with Home Assistant after Daikin upgraded the firmware to 2.8.0 and the native integration no longer works.  
This is fairly limited at the moment but it works


# Requirements
These python packages are required for the code to work:
`paho-mqtt`
`requests`

# Installation
Installation steps are very simple:
- Install the additional python modules
- Download the 3 files
- Update the ini file to suit your install
- Run `python3 main.py`

# Sample MQTT config in Home Assistant
```
mqtt:
  - climate:
      name: Studio Climate
      unique_id: studioac
      modes:
        - "off"
        - "cool"
        - "dry"
        - "heat"
        - "fan_only"
      temperature_command_topic: "climate/studio/settemperature"
      current_humidity_topic: "climate/studio/humidity"
      current_temperature_topic: "climate/studio/temperature"
      temperature_state_topic: "climate/studio/temperaturesp"
      mode_state_topic: "climate/studio/mode"
      precision: 0.5
```
