# Hass.io Community Store

![Logo][logo]

HACS gives you a powerful UI to handle downloads of custom needs.
This add-on is just a shortcut to install [hacs](https://hacs.xyz). 
**For easy-installation only.** 

***
## Installation
1. Add the repository URL via the Hassio Add-on Store Tab: **https://github.com/MickMake/HassioAddon**

2. Install and start the `Hass.io Community Store` add-on **once**. 

3. Check the logs; if everything OK, **Uninstall it**. 

4. Configure HACS [instruction here](https://hacs.xyz/docs/configuration/basic)

### Update
**NOTICE**: Components installed manual or outside this store will not be managed in component store.

**HACS** can update itself inside the store. You will need to restart Home Assistant to apply the update.

**Store Content** will refresh: At *startup* or every *500 minutes* after HA startup.

**Installed element** will be checked for updates: At *startup* or every *30 minutes* after HA startup.

### Startup
During the startup there will be a progressbar indicating that it's scanning for known repositories. This is completely normal, and you can still use it while it's working. 

***
### Licenses
Additional licenses for third-party components of this addon are available as part of the [LICENSE.md](https://github.com/MickMake/Addons/blob/main/hacs/docs/LICENSE.md) file.
### Credits
- [Home Assistant Community Store](https://hacs.xyz)

[logo]: https://github.com/MickMake/HassioAddon/raw/main/hacs/icon.png
