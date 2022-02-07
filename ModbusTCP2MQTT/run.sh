#!/usr/bin/env bashio


IP=$(bashio::config 'Inverter_IP')
PORT=$(bashio::config 'Inverter_port')
MODEL=$(bashio::config 'Model')
SCAN_INTERVAL=$(bashio::config 'Scan_interval')
SCAN_TIMEOUT=$(bashio::config 'Scan_timeout')
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

exec python3 /ModbusTCP.py --ip=${IP} --port=${PORT} --model=${MODEL} --mqtt_host=${MQTT_HOST} --mqtt_port=${MQTT_PORT} --mqtt_user=${MQTT_USER} --mqtt_pass=${MQTT_PASS} --scan=${SCAN_INTERVAL} --timeout=${SCAN_TIMEOUT} --log_level=${LOG_LEVEL}