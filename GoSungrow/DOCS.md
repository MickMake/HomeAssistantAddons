# GoSungrow for [Home Assistant](https://www.home-assistant.io/).

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-shield]: https://img.shields.io/badge/i386-no-red.svg

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]
![Supports armhf Architecture][armhf-shield]
![Supports armv7 Architecture][armv7-shield]
![Supports i386 Architecture][i386-shield]


## Configuration
Install in the usual manner.

1. Go to Configuration -> Add-ons.

![Install add-on](https://github.com/MickMake/HomeAssistantAddons/raw/main/GoSungrow/docs/ScreenShot1.png)

2. Add the MickMake HA Repository.

![Install add-on](https://github.com/MickMake/HomeAssistantAddons/raw/main/GoSungrow/docs/ScreenShot2.png)

![Install add-on](https://github.com/MickMake/HomeAssistantAddons/raw/main/GoSungrow/docs/ScreenShot3.png)

3. Once added, it will appear in the list of add-on repositories.

![Install add-on](https://github.com/MickMake/HomeAssistantAddons/raw/main/GoSungrow/docs/ScreenShot4.png)

![Install add-on](https://github.com/MickMake/HomeAssistantAddons/raw/main/GoSungrow/docs/ScreenShot4b.png)

4. Install the add-on and click Configuration.

![Install add-on](https://github.com/MickMake/HomeAssistantAddons/raw/main/GoSungrow/docs/ScreenShot5.png)

![Install add-on](https://github.com/MickMake/HomeAssistantAddons/raw/main/GoSungrow/docs/ScreenShot5b.png)

5. Set the config options.

![Install add-on](https://github.com/MickMake/HomeAssistantAddons/raw/main/GoSungrow/docs/ScreenShot6.png)

The following options are mandatory:
- sungrow_user
- sungrow_password - Make sure you have created your account at https://isolarcloud.com/

- sungrow_mqtt_user
- sungrow_mqtt_password - Enter in your login details for HA.

You may have to set the following options. As of v3.0.0 if you leave the blank, it'll autoconfigure:
- sungrow_mqtt_host
- sungrow_mqtt_port

The rare occasion:
- sungrow_host - May need to be changed depending on which global server you connect to.
- sungrow_appkey - Just don't. Really don't, but if you want to hack. Then do!
- sungrow_timeout - Useful if your iSolarCloud global gateway is slow/unreachable.
- sungrow_debug - If you REALLY want to see some noise. Just leave it unset.

5. Start it up!

![Install add-on](https://github.com/MickMake/HomeAssistantAddons/raw/main/GoSungrow/docs/ScreenShot7.png)


## Adding a specific MQTT user account.

If you want to add a different user for MQTT, then here's how.

1. Click on "Add User".
![Install add-on](https://github.com/MickMake/HomeAssistantAddons/raw/main/GoSungrow/docs/mqtt1.png)

2. Create your user.
![Install add-on](https://github.com/MickMake/HomeAssistantAddons/raw/main/GoSungrow/docs/mqtt2.png)
![Install add-on](https://github.com/MickMake/HomeAssistantAddons/raw/main/GoSungrow/docs/mqtt3.png)

3. For extra security, toggle "Can only login from olocal network."
![Install add-on](https://github.com/MickMake/HomeAssistantAddons/raw/main/GoSungrow/docs/mqtt4.png)


## Lovelace examples

[These are the Lovelace YAML files](https://github.com/MickMake/HomeAssistantAddons/raw/main/GoSungrow/docs/lovelace) and images I use for my HA instance:

You'll need to modify the ps_id and ps_keys within these files to display the correct info. Any text editor can do a global search and replace.

You can use the GoSungrow tool to get this info:

`GoSungrow show ps tree`

Also grab the images from the [images directory](https://github.com/MickMake/HomeAssistantAddons/raw/main/GoSungrow/docs/lovelace/images) and place them in your /config/www directory.


## About GoSunGrow
See the docs here [GoSunGrow](https://github.com/MickMake/GoSunGrow/)
