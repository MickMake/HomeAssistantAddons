
# Hassio add-on Repository
This repository contains Hass.io add-ons. All add-ons in this repository are tested on Hass.io, Home Assistant Core installation is not supported.

### Installation
1. Navigate in your Home Assistant frontend to <kbd>Supervisor</kbd> -> <kbd>Add-on Store</kbd>.

2. Click the 3-dots menu at upper right <kbd>...</kbd> > <kbd>Repositories</kbd> and add this repository's URL: [https://github.com/MickMake/HassioAddon](https://github.com/MickMake/HassioAddon)

   <img src="images/add_repo.png" width="300"/>

3. Scroll down the page to find the new repository, and click the new add-on named you want. Ex:

   <img src="images/repo_ss.png" width="429"/>

4. Click <kbd>Install</kbd> and give it a few minutes to finish downloading.

5. Follow the instruction for each addon to configures


### Updating
Enable `Auto update` on the desired add-on or browse Hassio Add-on Store Tab to check for update

# Add-ons in this Repository

### Home Assistant Community Store
HACS gives you a powerful UI to handle downloads of all your custom needs.

Developer info [hacs.xyz](https://hacs.xyz/).

### Home Assistant Google Drive Backup
This add-on will upload snapshot files from your hass.io (.tar files created by the hass.io SnapShot) to your Google Drive.

Forked from [hassio-google-drive-backup](https://github.com/sabeechen/hassio-google-drive-backup).

### Zigbee2MQTT
Communication with zigbee endpoint using CC2530/ CC2531 / CC2581 chip.
You will need a Zigbee module flashed coordinator firmware in order to work.

Developer info [zigbee2mqtt.io](https://www.zigbee2mqtt.io/).

### TTLock2MQTT
Control TTLock and get lock status. This addon based on tonyldo Addon with improvement on auto token refresh.
Need `Gateway G2` and TTLOCK API token in order to work.
Get Token [intructions](https://github.com/tonyldo/ttlockio)
Developer info [TTLock2MQTT](https://github.com/MickMake/TTLock2MQTT)

### ModbusTCP2MQTT
This addon support SMA & Sungrow Solar Inverter to publish data to MQTT Broker. 
This add on based on [ModbusTCP2MQTT](https://github.com/MickMake/ModbusTCP2MQTT)

### ModbusWeb2MQTT
This addon support SMA & Sungrow Solar Inverter to publish data to MQTT Broker. 
This add on based on [ModbusWeb2MQTT](https://github.com/MickMake/ModbusWeb2MQTT)


# Custom Component
**NOTICE**: It's recommend to use **Community Store Add-on** to install `custom components`. Component installed manually will not be mananged in component store.

If you found useful component and want to share, don't hesitate let us know.

### Simple Installation
1. Make sure you've the [Community Store](https://github.com/MickMake/HassioAddon/tree/main/hacs) installed and working.
2. Navigate to the Store (on the menu bar), select Store 
3. Search and select **component** you want and install.
4. Refer to component documents for configure and usage
5. Restart Home-Assistant.

### Manual Installation
1. Download component and extract to `component_name` folder
2. Create a new folder called `component_name` inside your ha_config_dir/custom_components directory and copy the all the files from `component_name` to it.
3. Refer to component documents for configure and usage
4. Restart Home-Assistant.

### Updating
Use Custom Component Store to update your card

## Useful Components in this Store

#### SmartIR
Modify from SmartIR for better service `media_player.select_source` 

You can find the [details here](https://github.com/MickMake/smartIR)

#### Zing MP3
Play media on zing.mp3.vn. Offer 2 services: `zing_mp3.play` and `zing_mp3.play_top100`

You can find the [details here](https://github.com/MickMake/zing_mp3)



# Lovelace UI Custom Card (Plugin)
If you found useful card and want to share, don't hesitate let us know.

### Installation
1. Make sure you've the [Community Store](https://github.com/MickMake/HassioAddon/tree/main/hacs) installed and working.
2. Navigate to the Store (on the menu bar), select Store 
3. Search and select **cards** you want and install.
4. Add reference to **cards** inside your `ui-lovelace.yaml` or at the top of the *raw config editor UI*. Instruction 
shown when you install card. For ex, when install mini-graph-card, you need to add:

  ```yaml
  resources:
    - type: module
      url: /community_plugin/mini-graph-card/mini-graph-card.js
  ```
  
5. Restart Hass UI, you can now use use the `custom-card`.

### Updating
Use Component Store to update your card

*You may need to empty the browsers cache if you have problems loading the updated card.*

## Some useful Cards in this Repository

### Mini Graph Card
You can find the [details here](https://github.com/kalkih/mini-graph-card)
### Simple Thermostat
You can find the [details here](https://github.com/nervetattoo/simple-thermostat)
### Mini Media Player
You can find the [details here](https://github.com/kalkih/mini-media-player)

# Credit

This repository is credit to MagnetVN, LLC

Copyright (c) 2019, ttvtien

[logo]: https://github.com/MickMake/HassioAddon/raw/main/images/Logo.png
