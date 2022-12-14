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

cd /usr/local/bin
ARCH="$(uname -m)"
case "${ARCH}" in
	'amd64'|'x86_64')
		ARCH="amd64"
		;;

	'aarch64'|'armhf'|'armv7'|'arm64')
		ARCH="arm64"
		;;

	*)
		bashio::log.error "Architecture not supported"
		exit 1
esac

curl -s https://api.github.com/repos/MickMake/GoSungrow/releases/latest | grep "browser_download_url.*$(uname -m).deb" \
| head -1 \
| cut -d : -f 2,3 \
| tr -d \" \
| wget --show-progress -qi - \
|| echo "-> Could not download the latest version of '${REPO}' for your architecture." # if you're polite


wget -O- https://github.com/MickMake/GoSungrow/releases/download/v${GOSUNGROW_VERSION}/GoSungrow-linux_${ARCH}.tar.gz | tar zxvf - GoSungrow

chmod a+x GoSungrow

