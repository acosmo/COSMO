#!/bin/bash

# Load configuration
source "$(dirname "$0")/config.sh"

# Read one message from each topic
SOLAR=$(mosquitto_sub -h "$MQTT_HOST" -u "$MQTT_USER" -P "$MQTT_PASS" -t "cosmo" -C 1)
CAR=$(mosquitto_sub -h "$MQTT_HOST" -u "$MQTT_USER" -P "$MQTT_PASS" -t "rover/power" -C 1)

# Default to zero if empty
SOLAR=${SOLAR:-0}
CAR=${CAR:-0}

# Calculate solar percentage
SOLAR_PCT=$(( SOLAR * 100 / SOLAR_MAX_CAPACITY ))

# Clamp to 0-100
if [ "$SOLAR_PCT" -gt 100 ]; then
    SOLAR_PCT=100
elif [ "$SOLAR_PCT" -lt 0 ]; then
    SOLAR_PCT=0
fi

curl -X POST https://rest.ably.io/channels/nova/messages \
    -u "$ABLY_KEY" \
    -H "Content-Type: application/json" \
    --data "{
      \"name\":\"cURL\",
      \"data\":{
        \"solar_pct\":\"$SOLAR_PCT\",
        \"solar\":\"$SOLAR\",
        \"car_pct\":\"98\",
        \"car\":\"$CAR\",
        \"battery_pct\":\"100\",
        \"battery\":\"100\",
        \"house\":\"350\",
        \"grid\":\"100\"
      }
    }"