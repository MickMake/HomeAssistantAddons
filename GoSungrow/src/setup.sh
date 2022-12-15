#!/usr/bin/env bashio
set -e

checkExit()
{
	EXIT="$?"
	if [ "${EXIT}" != "0" ]
	then
		bashio::log.error "# GoSungrow: FAILED to install, please raise a GitHub issue."
		exit ${EXIT}
	fi
}


apk update; checkExit
apk add --no-cache --virtual gosungrow.persist jq wget curl; checkExit

chmod a+x /usr/local/bin/getRelease.sh /usr/local/bin/run.sh /usr/local/bin/setup.sh

/usr/local/bin/getRelease.sh

