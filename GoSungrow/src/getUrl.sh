#!/usr/bin/env bashio
set -e

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

wget -O- https://github.com/MickMake/GoSungrow/releases/download/v2.2.0/GoSungrow-linux_${ARCH}.tar.gz | tar zxvf - GoSungrow

chmod a+x GoSungrow

