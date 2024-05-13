#!/usr/bin/env bashio

export DAIKIN_MQTT_DATA="/config/daikin-mqtt"

if ! bashio::fs.file_exists "$DAIKIN_MQTT_DATA/configuration.yaml"; then
  mkdir -p "$DAIKIN_MQTT_DATA" || bashio::exit.nok "Could not create $DAIKIN_MQTT_DATA"

   cat <<EOF > "$DAIKIN_MQTT_DATA/configuration.yaml"
general:
mqtt:
  server:
  port: 1883
  username:
  password:
units:
  - name:
    address:
EOF
fi

export CONFIG_PATH="$DAIKIN_MQTT_DATA/configuration.yaml"

bashio::log.info "Starting Daikin MQTT..."

exec python3 /app/main.py
