wincc_alarmer
=======================

This python module provides functionality to periodically query the WinCC
alarm archives for alarms. Found alarms can be sent via email or as syslog 
messages.

## Functions

1. Poll WinCC alarm archives.
2. Email or syslog found alarms.


## Prerequisites

### Local
1. python 2.7
2. python modules
	* pywincc
    * click
    * jinja2
    * premailer
3. WinCC
    * WinCC Connectivity Pack Client or Connectivity Station(?)
    * Modify the registry (see below)

#### Registry modification
In order to enable the adodbapi module to work with the WINCCOLEDBProvider.1 proceed as follows.
Open 'regedit' and search for 'WINCCOLEDBProvider'. The first result should lead to  
HKEY_LOCAL_MACHINE - SOFTWARE - Classes - CLSID - Some string (e.g. {3EE5243C-3779-4545-A573-F60ABC436816}).
Now, at this key, add a DWORD value with name "OLEDB_SERVICES" and value 0xffffffff.
See screenshot 'regedit_oledb_services.png'.

![Win Registry modifications for WINCCOLEDBProvider.1](regedit_oledb_services.png)

### Remote machine
1. WinCC 7.0 (previous or newer versions may also work)
2. VPN connection to remote machine (e.g. OpenVPN)
3. Firewall settings to allow connection from remote machine