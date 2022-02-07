ARG BUILD_FROM
FROM $BUILD_FROM
ENV LANG C.UTF-8

# Build arugments
ARG BUILD_VERSION
ARG BUILD_ARCH

COPY models/ /
COPY requirements.txt /tmp/
COPY run.sh /
COPY ModbusTCP.py /

# Install requirements for add-on
RUN apk add --no-cache python3-dev py3-pip g++
RUN pip3 install -r /tmp/requirements.txt
RUN chmod a+x /run.sh

CMD ["/run.sh"]

LABEL \ 
    io.hass.name="ModbusTCP2MQTT" \
    io.hass.description="Sungrow-SMA Solar inverter communication Addon" \
    io.hass.version=${BUILD_VERSION} \
    io.hass.type="addon" \
    io.hass.arch=${BUILD_ARCH}
