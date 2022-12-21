#!/usr/bin/env bashio
# set -e

export HOME="/data"
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


export GOSUNGROW_USER="$(jq --raw-output '.sungrow_user // empty' ${CONFIG_PATH})"
export GOSUNGROW_PASSWORD="$(jq --raw-output '.sungrow_password // empty' ${CONFIG_PATH})"
export GOSUNGROW_HOST="$(jq --raw-output '.sungrow_host // empty' ${CONFIG_PATH})"


export GOSUNGROW_APPKEY="$(jq --raw-output '.sungrow_appkey // empty' ${CONFIG_PATH})"
export GOSUNGROW_DEBUG="$(jq --raw-output '.debug // empty' ${CONFIG_PATH})"
export GOSUNGROW_TIMEOUT="$(jq --raw-output '.sungrow_timeout|tostring + "s" // empty' ${CONFIG_PATH})"


export GOSUNGROW_MQTT_HOST=""
export GOSUNGROW_MQTT_PORT=""
export GOSUNGROW_MQTT_USER=""
export GOSUNGROW_MQTT_PASSWORD=""
if bashio::services.available "mqtt"
then
	bashio::log.info "MQTT services is available!"
	GOSUNGROW_MQTT_HOST="$(bashio::services mqtt "host")"
	GOSUNGROW_MQTT_PORT="$(bashio::services mqtt "port")"
	GOSUNGROW_MQTT_USER="$(bashio::services mqtt "username")"
	GOSUNGROW_MQTT_PASSWORD="$(bashio::services mqtt "password")"
fi

GOSUNGROW_MQTT_HOST="$(jq --raw-output --arg default "${GOSUNGROW_MQTT_HOST}" '.mqtt_host // empty | select(. != "") // $default' ${CONFIG_PATH})"
if [ -z "${GOSUNGROW_MQTT_HOST}" ]
then
	# bashio::log.error "No MQTT host defined and none could be auto-detected."
	GOSUNGROW_MQTT_HOST="core-mosquitto"
fi


GOSUNGROW_MQTT_PORT="$(jq --raw-output --arg default "${GOSUNGROW_MQTT_PORT}" '.mqtt_port // empty | select(. != "") // $default' ${CONFIG_PATH})"
if [ -z "${GOSUNGROW_MQTT_PORT}" ]
then
	GOSUNGROW_MQTT_PORT="1883"
fi


GOSUNGROW_MQTT_USER="$(jq --raw-output --arg default "${GOSUNGROW_MQTT_USER}" '.mqtt_user // empty | select(. != "") // $default' ${CONFIG_PATH})"
if [ -z "${GOSUNGROW_MQTT_USER}" ]
then
	bashio::log.warning "MQTT user is empty. I'm guessing this is what you wanted?"
fi


GOSUNGROW_MQTT_PASSWORD="$(jq --raw-output --arg default "${GOSUNGROW_MQTT_PASSWORD}" '.mqtt_password // empty | select(. != "") // $default' ${CONFIG_PATH})"
if [ -z "${GOSUNGROW_MQTT_PASSWORD}" ]
then
	bashio::log.warning "MQTT password is empty. I'm guessing this is what you wanted?"
fi


bashio::log.info "Writing GoSungrow config ..."
/usr/local/bin/GoSungrow config write
checkExit


bashio::log.info "Login to iSolarCloud using gateway ${GOSUNGROW_HOST} ..."
/usr/local/bin/GoSungrow api login
checkExit


bashio::log.info "Syncing data from gateway ${GOSUNGROW_HOST} ..."
/usr/local/bin/GoSungrow mqtt run 
# /usr/local/bin/GoSungrow mqtt sync 
checkExit


bashio::log.info "GoSungrow exited without error ... strange ..."
sleep 5


# DEBUG...
#sleep 99999999
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
 
