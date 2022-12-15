#!/usr/bin/env bashio
# set -e

export CONFIG_PATH="/data/options.json"
export HOME="/data"

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

export GOSUNGROW_USER GOSUNGROW_PASSWORD GOSUNGROW_HOST
export GOSUNGROW_APPKEY GOSUNGROW_DEBUG GOSUNGROW_TIMEOUT
export GOSUNGROW_MQTT_HOST GOSUNGROW_MQTT_PORT GOSUNGROW_MQTT_USER GOSUNGROW_MQTT_PASSWORD


GOSUNGROW_USER="$(jq --raw-output '.sungrow_user // empty' ${CONFIG_PATH})"
GOSUNGROW_PASSWORD="$(jq --raw-output '.sungrow_password // empty' ${CONFIG_PATH})"
GOSUNGROW_HOST="$(jq --raw-output '.sungrow_host // empty' ${CONFIG_PATH})"
GOSUNGROW_APPKEY="$(jq --raw-output '.sungrow_appkey // empty' ${CONFIG_PATH})"

GOSUNGROW_DEBUG="$(jq --raw-output '.debug // empty' ${CONFIG_PATH})"
GOSUNGROW_TIMEOUT="$(jq --raw-output '.sungrow_timeout|tostring + "s" // empty' ${CONFIG_PATH})"


export GOSUNGROW_MQTT_HOST="$(bashio::services mqtt "host")"
GOSUNGROW_MQTT_HOST="$(jq --raw-output --arg default "${GOSUNGROW_MQTT_HOST}" '.mqtt_host // empty | select(. != "") // $default' ${CONFIG_PATH})"
if [ -z "${GOSUNGROW_MQTT_HOST}" ]
then
	bashio::log.error "No MQTT host defined and none could be auto-detected."
	exit -1
fi


GOSUNGROW_MQTT_PORT="$(jq --raw-output '.mqtt_port // empty' ${CONFIG_PATH})"
GOSUNGROW_MQTT_PORT="$(jq --raw-output --arg default "${GOSUNGROW_MQTT_PORT}" '.mqtt_port // empty | select(. != "") // $default' ${CONFIG_PATH})"
if [ -z "${GOSUNGROW_MQTT_PORT}" ]
then
	GOSUNGROW_MQTT_PORT="1883"
fi


GOSUNGROW_MQTT_USER="$(bashio::services mqtt "username")"
GOSUNGROW_MQTT_USER="$(jq --raw-output --arg default "${GOSUNGROW_MQTT_USER}" '.mqtt_user // empty | select(. != "") // $default' ${CONFIG_PATH})"


GOSUNGROW_MQTT_PASSWORD="$(bashio::services mqtt "password")"
GOSUNGROW_MQTT_PASSWORD="$(jq --raw-output --arg default "${GOSUNGROW_MQTT_PASSWORD}" '.mqtt_password // empty | select(. != "") // $default' ${CONFIG_PATH})"


bashio::log.info "Writing GoSungrow config ..."
/usr/local/bin/GoSungrow config write
checkExit


bashio::log.info "Login to iSolarCloud using gateway ${GOSUNGROW_HOST} ..."
/usr/local/bin/GoSungrow api login
# checkExit


bashio::log.info "Syncing data from gateway ${GOSUNGROW_HOST} ..."
# /usr/local/bin/GoSungrow mqtt sync
# checkExit


bashio::log.info "GoSungrow exited without error ..."

#if ! bashio::services.available "mqtt"
#then
#    echo "No internal MQTT service found. Please install Mosquitto broker"
#    bashio::log.error "No internal MQTT service found. Please install Mosquitto broker"
#fi
#
#  echo "host: $(bashio::services "mqtt" "host")"
#  echo "password: $(bashio::services "mqtt" "password")"
#  echo "port: $(bashio::services "mqtt" "port")"
#  echo "username: $(bashio::services "mqtt" "username")"
#
#  bashio::log.info "host: $(bashio::services "mqtt" "host")"
#  bashio::log.info "password: $(bashio::services "mqtt" "password")"
#  bashio::log.info "port: $(bashio::services "mqtt" "port")"
#  bashio::log.info "username: $(bashio::services "mqtt" "username")"
#
#echo "################################################################################"
#set > /tmp/d1
#echo "################################################################################"
#env >> /tmp/d1
#echo "################################################################################"
#ping core-mosquitto
#
#echo "SUPERVISOR_TOKEN:${SUPERVISOR_TOKEN}"
#curl -sSL -H "Authorization: Bearer $SUPERVISOR_TOKEN" http://supervisor/services/mqtt

sleep 99999999
 
