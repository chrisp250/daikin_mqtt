# MQTT integration for Daikin airconditoners
I developed this integration to get my AC to work again with Home Assistant after Daikin upgraded the firmware to 2.8.0 and the native integration no longer works.  
This is fairly basic at the moment but I'm hoping it fills the gap while a more polished solution is available

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Ffoxdalas%2Fdaikin_mqtt)


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

# Docker build
Build the image:
- `docker build -t daikin_mqtt .`

Run the image:
- Update the daikin.ini file to suit your install
- `docker run -d -v $(pwd)/daikin.ini:/usr/src/app/daikin.ini daikin_mqtt`

# Sample MQTT config in Home Assistant
```
mqtt:
  - climate:
      name: Studio Climate
      modes:
        - "off"
        - "cool"
        - "dry"
        - "heat"
        - "fan_only"
        - "auto"
      fan_modes:
        - "auto"
        - "Quiet"
        - "1"
        - "2"
        - "3"
        - "4"
        - "5"        
      temperature_command_topic: "climate/studio/settemperature"
      current_humidity_topic: "climate/studio/humidity"
      current_temperature_topic: "climate/studio/temperature"
      temperature_state_topic: "climate/studio/temperaturesp"
      mode_state_topic: "climate/studio/mode"
      mode_command_topic: "climate/studio/modecommand"
      fan_mode_state_topic: "climate/studio/fanmode"
      temperature_command_topic: "climate/studio/temperaturecommand"
      precision: 0.5
```

# What's implemented
The integration reads data from the AC unit and pushes it to MQTT.  
The parameters it reads from the unit are:
- Unit mode (off, heating, cooling, fan, dry, auto)
- Room temperature
- Room humidity
- Temperature setpoint (when in heating or cooling mode)
- Fan mode: (auto, quiet, 1, 2, 3, 4, 5)

Controls functionality is limited to switching the unit to different modes: off,fan,heat,cool,auto,dry, and setting the temperature only when in heating or cooling mode at this stage.
Enjoy!

# Ask
If you find my app useful, please consider upvoting my [feauture request](https://community.home-assistant.io/t/request-for-expiry-after-option-in-mqtt-hvac-integration/726390) for an `expiry_after` option for the MQTT HVAC integration for Home Assistant.  
This will allow Home Assistant show the device offline if it stops receiving updates for a period of time.  
Thank you
