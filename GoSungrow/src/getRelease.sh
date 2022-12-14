#!/usr/bin/env bashio
set -e

function checkExit()
{
	EXIT="$?"
	if [ "${EXIT}" != "0" ]
	then
		echo bashio::log.error "# GoSungrow: FAILED to install, please raise a GitHub issue."
		exit ${EXIT}
	fi
}

function Get() {
	# Get(url, repo, arch, tag)
	wget -N "$1"
	RETURN="$(jq -r --arg REPO "$2" --arg ARCH "$3" '.assets[] | select(.name|match($REPO + "-" + $ARCH + ".tar.gz$")) | '$4 latest)"
}

################################################################################

HW="$(uname -m)"
case "${HW}" in
	'amd64'|'x86_64')
		HW="amd64"
		;;

	'aarch64'|'armv8'|'arm64')
		HW="arm64"
		;;

	'armv7'|'armhf')
		HW="arm_6"
		;;

	*)
		echo bashio::log.error "Hardware not supported"
		exit 1
		;;
esac

OS="$(uname -s)"
case "${OS}" in
	'Darwin'|'darwin')
		OS="darwin"
		;;

	'Linux'|'linux')
		OS="linux"
		;;

	*)
		echo bashio::log.error "O/S not supported"
		exit 1
		;;
esac

ARCH="${OS}_${HW}"

REPO="GoSungrow"
URL="https://api.github.com/repos/MickMake/${REPO}/releases/latest"

echo bashio::log.info "Searching for architecture type \"${ARCH}\" on repo \"${URL}\" ..."

Get "${URL}" "${REPO}" "${ARCH}" ".name"
if [ -z "${RETURN}" ]
then
	echo bashio::log.error "Architecture not supported. Please raise an issue on GitHub."
	exit 1
fi
FILENAME="${RETURN}"


Get "${URL}" "${REPO}" "${ARCH}" ".browser_download_url"
if [ -z "${RETURN}" ]
then
	echo bashio::log.error "Architecture not supported. Please raise an issue on GitHub."
	exit 1
fi


echo bashio::log.info "Downloading file \"${FILENAME}\" from repo \"${URL}\" ..."
# cd /tmp
# wget -O- https://github.com/MickMake/GoSungrow/releases/download/v${GOSUNGROW_VERSION}/GoSungrow-linux_${ARCH}.tar.gz | tar zxvf - GoSungrow
wget --show-progress -q "${RETURN}"
checkExit


echo bashio::log.info "Extracting file \"${FILENAME}\" ..."
tar zxvf "${FILENAME}" "${REPO}"
checkExit


echo bashio::log.info "Tidy up ..."
chmod a+x "${REPO}"
mv "${REPO}" /usr/local/bin
rm -f "${FILENAME}"
ls -l "/usr/local/bin/${REPO}"

echo bashio::log.info "Done! You're ready to go!"

