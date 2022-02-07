## Installation

1. Add the repository URL via the Hassio Add-on Store Tab: **https://github.com/TenySmart/HassioAddon**
2. Configure the "ModbusTCP2MQTT" add-on.
3. Start the "ModbusTCP2MQTT" add-on.

## Configuration

**Note**: _Remember to restart the add-on when the configuration is changed._

```yaml
Inverter_IP: Your Inverter IP
Inverter_port: Your Inverter Port (Default: 502)
Model: one of supported models
Scan_interval: 10-600
Scan_timeout: 3->60
log_level: INFO|WARNING|DEBUG
```

### Options: `Scan_interval` 
Increase scan_interval in case you get "Modbus connection failed" at run time.

### Option: `Log_level`

- `debug`: Shows detailed debug information.
- `info`: Default informations.
- `warning`: Little alerts.

### MQTT Broker:
Your MQTT Broker address and credentials. If you don't know what this is, install this addon:
https://github.com/home-assistant/hassio-addons/tree/master/mosquitto

