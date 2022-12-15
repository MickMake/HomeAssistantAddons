#!/usr/bin/env bashio
set -e

export CONFIG_PATH="/data/options.json"
export GOSUNGROW_CONFIG="$HOME/.GoSungrow/config.json"

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

id
ls -la $HOME


bashio::log.info "Setting up GoSungrow config ..."

export GOSUNGROW_USER="$(jq --raw-output '.sungrow_user // empty' ${CONFIG_PATH})"
export GOSUNGROW_PASSWORD="$(jq --raw-output '.sungrow_password // empty' ${CONFIG_PATH})"
export GOSUNGROW_HOST="$(jq --raw-output '.sungrow_host // empty' ${CONFIG_PATH})"
export GOSUNGROW_APPKEY="$(jq --raw-output '.sungrow_appkey // empty' ${CONFIG_PATH})"

export GOSUNGROW_DEBUG="$(jq --raw-output '.debug // empty' ${CONFIG_PATH})"
export GOSUNGROW_TIMEOUT="$(jq --raw-output '.sungrow_timeout|tostring + "s" // empty' ${CONFIG_PATH})"

export GOSUNGROW_MQTT_HOST="$(bashio::services mqtt "host")"
GOSUNGROW_MQTT_HOST="$(jq --raw-output --arg default "${GOSUNGROW_MQTT_HOST}" '.mqtt_host // empty | select(. != "") // $default' ${CONFIG_PATH})"

export GOSUNGROW_MQTT_PORT="$(jq --raw-output '.mqtt_port // empty' ${CONFIG_PATH})"

export GOSUNGROW_MQTT_USER="$(bashio::services mqtt "username")"
GOSUNGROW_MQTT_USER="$(jq --raw-output --arg default "${GOSUNGROW_MQTT_USER}" '.mqtt_user // empty | select(. != "") // $default' ${CONFIG_PATH})"

export GOSUNGROW_MQTT_PASSWORD="$(bashio::services mqtt "password")"
GOSUNGROW_MQTT_PASSWORD="$(jq --raw-output --arg default "${GOSUNGROW_MQTT_PASSWORD}" '.mqtt_password // empty | select(. != "") // $default' ${CONFIG_PATH})"


#DEETS="
#	GOSUNGROW_HOST = \"${GOSUNGROW_HOST}\"
#	GOSUNGROW_USER = \"${GOSUNGROW_USER}\"
#	GOSUNGROW_PASSWORD = \"${GOSUNGROW_PASSWORD}\"
#	GOSUNGROW_APPKEY = \"${GOSUNGROW_APPKEY}\"
#	GOSUNGROW_DEBUG = \"${GOSUNGROW_DEBUG}\"
#	GOSUNGROW_TIMEOUT = \"${GOSUNGROW_TIMEOUT}\"
#
#	GOSUNGROW_MQTT_HOST = \"${GOSUNGROW_MQTT_HOST}\"
#	GOSUNGROW_MQTT_PORT = \"${GOSUNGROW_MQTT_PORT}\"
#	GOSUNGROW_MQTT_USER = \"${GOSUNGROW_MQTT_USER}\"
#	GOSUNGROW_MQTT_PASSWORD = \"${GOSUNGROW_MQTT_PASSWORD}\"
#"
#bashio::log.info "DEETS: $DEETS"
#cat $CONFIG_PATH
#ls -l $CONFIG_PATH


bashio::log.info "Writing GoSungrow config ..."
set -x
/usr/local/bin/GoSungrow config write
set +x
checkExit


bashio::log.info "Login to iSolarCloud using gateway ${GOSUNGROW_HOST} ..."
/usr/local/bin/GoSungrow api login
checkExit


bashio::log.info "Syncing data from gateway ${GOSUNGROW_HOST} ..."
/usr/local/bin/GoSungrow mqtt sync
checkExit


bashio::log.info "GoSungrow exited without error ..."

ls -la $HOME
ls -la $HOME/.GoSungrow .
ls -l $HOME/.GoSungrow/config.json config.json
cat $HOME/.GoSungrow/config.json config.json
