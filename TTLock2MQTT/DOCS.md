# TTLock2MQTT Add-on

Integrating your TTLock devices with Home Assistant over MQTT

## Installation

1. Add the repository URL via the Hassio Add-on Store Tab: **https://github.com/TenySmart/HassioAddon**
2. Follow this [intructions](https://github.com/tonyldo/ttlockio) to get your `TTLOCK_CLIENT_ID` and `TTLOCK_CLIENT_SECRECT`
3. Configure the "TTLock2MQTT" add-on.
4. Start the "TTLock2MQTT" add-on.

## Configuration

**Note**: _Remember to restart the add-on when the configuration is changed._


```yaml
TTLock_username: YOUR_TTLOCK_DEVELOPER_ACCOUNT
TTLock_password: YOUR_TTLOCK_DEVELOPER_PASSWORD
TTLock_client_Id: YOUR_TTLOCK_CLIENT_APP
TTLock_client_secrect: YOUR_TTLOCK_CLIENT_SECRET
Scan_interval: 60
Log_level: info
```

### Options: `TTLock_username` *and* `TTLock_password`
Your developer account you created.

### Options: `TTLock_client_Id` *and* `TTLock_client_secrect`
You need to wait for your app to be reviewed. It will takes several days.

### Option: `Log_level`

- `debug`: Shows detailed debug information.
- `info`: Default informations.
- `warning`: Little alerts.
- `error`:  Only errors.

### MQTT Broker:
If you don't know what this is, install this addon:
https://github.com/home-assistant/hassio-addons/tree/master/mosquitto
