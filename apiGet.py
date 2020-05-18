#!/usr/bin/env python3

'''
************************************************************
This script is used to pull the available devices from 
Netbox and place them into their appropriate groups within
Rancid.  

Author: Charles Allen
Date: 12 May 2020
************************************************************
'''


import json
import requests

api_token = '<api_token>'
api_url_base = 'https://<URL>/api/dcim/devices/?role='
api_roles = ['netbox_roles']
config_base_path = "/usr/local/rancid/var/"


def configOutput(theRole, theOutput):

	'''
	*****************************************************************
	Subroutine is used to take the JSON output from the main routine
	and develop the needed output for the Rancid router.db file
	*****************************************************************
	'''
	netbox_role = theRole
	api_output = theOutput
	defOutput = ""

	for i in api_output['results']:

		device_type = i['device_type']['slug']
		
		if (i['primary_ip'] == None):
			continue;

		defOutput = defOutput + "{};{};up\n".format(i['name'],getRole(netbox_role,device_type))

	return defOutput

def getRole(theRole, theDeviceType):

	'''
	*****************************************************************
	Subroutine is used to create the needed Rancid type for the 
	router.db file.  Most use the type associated with their device
	role.  However, there are a handful of types that require a 
	configuration (i.e. Firewall and Core switch)
	*****************************************************************
	'''

	if theRole == "access-point":
		return "access-point"
	if theRole == "access-switch":
		return "access-switch"
	elif theRole == "cube":
		return "cube"
	elif theRole == "core-switch":
		return "core-switch"
	elif theRole == "dmvpn":
		return "dmvpn"
	elif theRole == "dmz-switch":
		return "dmz-switch"
	elif theRole == "dc-switch":
		return "nexus"
	elif theRole == "edge-router":
		return "edge-router"
	elif theRole == "firewall":
		return "firewall"
	elif theRole == "wireless-controller":
		return "wireless-controller"

def routerDbOutput (theRole, theConfig):

	'''
	*****************************************************************
	Subroutine writes the configuration to the appropriate router.db 
	file
	*****************************************************************
	'''

	config_path = "{}{}/router.db".format(config_base_path,theRole)

	with open (config_path, "wt") as f:
		f.write(theConfig)

'''
**********************************************
		Main Routine
**********************************************
'''

headers = {'Content-Type': 'application/json','Authorization': 'Token {0}'.format(api_token)}

for role in api_roles:

	api_url = api_url_base + role

	response = requests.get(api_url, headers=headers)
	output = json.loads(response.content.decode('utf-8'))

	if output['count'] == 0:
			continue
	
	routerDbOutput(role, configOutput(role, output))
