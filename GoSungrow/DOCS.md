# GoSungrow for [Home Assistant](https://www.home-assistant.io/).

![Supports aarch64 Architecture][aarch64-shield] ![Supports amd64 Architecture][amd64-shield] ![Supports armhf Architecture][armhf-shield] ![Supports armv7 Architecture][armv7-shield] ![Supports i386 Architecture][i386-shield]


## Configuration
Install in the usual manner.

1. Go to Configuration -> Add-ons.

![Install add-on](https://github.com/MickMake/HomeAssistantAddons/raw/main/GoSungrow/ScreenShot1.png)

2. Add the MickMake HA Repository.

![Install add-on](https://github.com/MickMake/HomeAssistantAddons/raw/main/GoSungrow/ScreenShot2.png)

![Install add-on](https://github.com/MickMake/HomeAssistantAddons/raw/main/GoSungrow/ScreenShot3.png)

3. Once added, it will appear in the list of add-on repositories.

![Install add-on](https://github.com/MickMake/HomeAssistantAddons/raw/main/GoSungrow/ScreenShot4.png)

4. Install the add-on and click Configuration.

![Install add-on](https://github.com/MickMake/HomeAssistantAddons/raw/main/GoSungrow/ScreenShot5.png)

5. Set the config options.

![Install add-on](https://github.com/MickMake/HomeAssistantAddons/raw/main/GoSungrow/ScreenShot6.png)

The following options are mandatory:
- sungrow_user
- sungrow_password

You may have to set these options:
- sungrow_mqtt_host
- sungrow_mqtt_port
- sungrow_mqtt_user
- sungrow_mqtt_password

The rare occasion:
- sungrow_host - May need to be changed depending on which global server you connect to.
- sungrow_appkey - Just don't. Really don't, but if you want to hack. Then do!
- sungrow_timeout - Useful if your iSolarCloud global gateway is slow/unreachable.
- sungrow_debug - If you REALLY want to see some noise. Just leave it unset.

## About GoSunGrow
See the docs here [GoSunGrow](https://github.com/MickMake/GoSunGrow/)
