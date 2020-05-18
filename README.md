# Rancid Special Purpose Scripts

## Outline
In my use of Rancid, there are special cases where Rancid cannot provide a needed set of functionality to fit my needs.  In those cases, I have developed the following Pythong scripts to fit my needs.

### API Get
Within my environment, we use Netbox as a source of truth.  I wanted it such that as we added devices into certain roles that it would automatically be populated into Rancid.  This simple script will execute an API get from Netbox to gather the needed data.  

Before use, the user must populate the following items:

+ *api_token*: an API token must be created within Netbox to allow access to the API.  
+ *api_url_base*: in my case, I wanted to focus on the device roles available within Netbox.  In this case, the base url is *https://<URL>/api/dcim/devices/?role=*.  I will then append the various device roles and iterate through them.  

### Bulk Change
Rancid is great in issuing a single or group of commands to a single device.  However, it lacks the functionality to do the same to a group of devices.  In this case, I wrote a Python script to query the existing *router.db* files to issues commands.  Please see the notes included the script for more information.  

In addition to those notes, please see the following assumptions:

1. The devices are already registered and used by Rancid under router.db files.  This script does not verify that the device listed in router.db is a Cisco device.
2. If the -u flag is not used, then the login information must be provided under the users .cloginrc file 
3. For the global variable baseDirPath, it must be pointed to the base directory where the config files are store. In this case, it is written for /usr/local/rancid/var. 

