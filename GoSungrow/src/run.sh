#!/usr/bin/env bashio
set -e

export CONFIG_PATH="/data/options.json"

checkExit()
{
	EXIT="$?"
	if [ "${EXIT}" != "0" ]
	then
		bashio::log.error "GoSungrow terminated with an error. Checking on things, please include this in any issue on GitHub ..."
		sleep 10
		set -x
		ls -lart /usr/local/bin/
		uname -a
		ifconfig
		ls -l ${CONFIG_PATH}
		cat ${CONFIG_PATH}
		/usr/local/bin/GoSungrow config read

		exit ${EXIT}
	fi
}


bashio::log.info "Setting up GoSungrow config ..."

export SUNGROW_HOST="$(bashio::config 'sungrow_host')"
if [ "${SUNGROW_HOST}" != "null" ]; then SUNGROW_HOST=""; fi

export SUNGROW_USER="$(bashio::config 'sungrow_user')"
if [ "${SUNGROW_USER}" != "null" ]; then SUNGROW_USER=""; fi

export SUNGROW_PASSWORD="$(bashio::config 'sungrow_password')"
if [ "${SUNGROW_PASSWORD}" != "null" ]; then SUNGROW_PASSWORD=""; fi

export SUNGROW_APPKEY="$(bashio::config 'sungrow_appkey')"
if [ "${SUNGROW_APPKEY}" != "null" ]; then SUNGROW_APPKEY=""; fi

export SUNGROW_DEBUG="$(bashio::config 'sungrow_debug')"
if [ "${SUNGROW_DEBUG}" != "null" ]; then SUNGROW_DEBUG=""; fi

export SUNGROW_TIMEOUT="$(bashio::config 'sungrow_timeout')"
if [ "${SUNGROW_TIMEOUT}" != "null" ]; then SUNGROW_TIMEOUT=""; fi


export SUNGROW_MQTT_HOST="$(bashio::services mqtt "host")"
SUNGROW_MQTT_HOST="$(bashio::config 'sungrow_mqtt_host' "${SUNGROW_MQTT_HOST}")"
if [ "${SUNGROW_MQTT_HOST}" != "null" ]; then SUNGROW_MQTT_HOST=""; fi

export SUNGROW_MQTT_PORT="$(bashio::config 'sungrow_mqtt_port')"
if [ "${SUNGROW_MQTT_PORT}" != "null" ]; then SUNGROW_MQTT_PORT=""; fi

export SUNGROW_MQTT_USER="$(bashio::services mqtt "username")"
SUNGROW_MQTT_USER="$(bashio::config 'sungrow_mqtt_user' "${SUNGROW_MQTT_USER}")"
if [ "${SUNGROW_MQTT_USER}" != "null" ]; then SUNGROW_MQTT_USER=""; fi

export SUNGROW_MQTT_PASSWORD="$(bashio::services mqtt "password")"
SUNGROW_MQTT_PASSWORD="$(bashio::config 'sungrow_mqtt_password' "${SUNGROW_MQTT_PASSWORD}")"
if [ "${SUNGROW_MQTT_PASSWORD}" != "null" ]; then SUNGROW_MQTT_PASSWORD=""; fi


DEETS="
	SUNGROW_HOST = \"${SUNGROW_HOST}\"
	SUNGROW_USER = \"${SUNGROW_USER}\"
	SUNGROW_PASSWORD = \"${SUNGROW_PASSWORD}\"
	SUNGROW_APPKEY = \"${SUNGROW_APPKEY}\"
	SUNGROW_DEBUG = \"${SUNGROW_DEBUG}\"
	SUNGROW_TIMEOUT = \"${SUNGROW_TIMEOUT}\"

	SUNGROW_MQTT_HOST = \"${SUNGROW_MQTT_HOST}\"
	SUNGROW_MQTT_PORT = \"${SUNGROW_MQTT_PORT}\"
	SUNGROW_MQTT_USER = \"${SUNGROW_MQTT_USER}\"
	SUNGROW_MQTT_PASSWORD = \"${SUNGROW_MQTT_PASSWORD}\"
"
bashio::log.info "DEETS: $DEETS"


bashio::log.info "Writing GoSungrow config ..."
/usr/local/bin/GoSungrow config write \
	--host="${SUNGROW_HOST}" \
	--user="${SUNGROW_USER}" \
	--password="${SUNGROW_PASSWORD}" \
	--appkey="${SUNGROW_APPKEY}" \
	--timeout="${SUNGROW_TIMEOUT}s" \
	--mqtt-host="${SUNGROW_MQTT_HOST}" \
	--mqtt-port="${SUNGROW_MQTT_PORT}" \
	--mqtt-user="${SUNGROW_MQTT_USER}" \
	--mqtt-password="${SUNGROW_MQTT_PASSWORD}" \
	--debug="${SUNGROW_DEBUG}"
checkExit


bashio::log.info "Config file now reads:"
/usr/local/bin/GoSungrow config read
checkExit


bashio::log.info "Login to iSolarCloud using gateway ${SUNGROW_HOST} ..."
/usr/local/bin/GoSungrow api login
checkExit


bashio::log.info "Syncing data from gateway ${SUNGROW_HOST} ..."
/usr/local/bin/GoSungrow mqtt sync
checkExit


bashio::log.info "GoSungrow exited without error ..."

