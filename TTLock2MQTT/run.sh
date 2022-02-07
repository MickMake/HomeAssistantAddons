#!/usr/bin/env bashio

TTLOCK_USER=$(bashio::config 'TTLock_username')
TTLOCK_PASS=$(bashio::config 'TTLock_password')
TTLOCK_CLIENT_ID=$(bashio::config 'TTLock_client_Id')
TTLOCK_SECRET=$(bashio::config 'TTLock_client_secrect')
SCAN_INTERVAL=$(bashio::config 'Scan_interval')
LOG_LEVEL=$(bashio::config 'Log_level')


if ! bashio::services.available "mqtt"; then
    bashio::exit.nok "No internal MQTT service found. Please install Mosquitto broker."
else
    MQTT_HOST=$(bashio::services mqtt "host")
    MQTT_PORT=$(bashio::services mqtt "port")
    MQTT_USER=$(bashio::services mqtt "username")
    MQTT_PASS=$(bashio::services mqtt "password")
    bashio::log.info "Configured'$MQTT_HOST' mqtt broker."
fi

exec python3 /ttlock_adapter.py --tt_user=${TTLOCK_USER} --tt_pass=${TTLOCK_PASS} --tt_id=${TTLOCK_CLIENT_ID} --tt_secret=${TTLOCK_SECRET}  --mqtt_host=${MQTT_HOST} --mqtt_port=${MQTT_PORT} --mqtt_user=${MQTT_USER} --mqtt_pass=${MQTT_PASS} --scan=${SCAN_INTERVAL} --log_level=${LOG_LEVEL}