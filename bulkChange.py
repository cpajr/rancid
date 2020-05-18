#!/usr/bin/env python3

import json
import requests
import argparse
import os.path
import sys
from getpass import getpass

'''
************************************************************
This script is used push bulk changes to devices registered
with Rancid through the Rancid script clogin.  This script
is exclusive for use with Cisco only devices.  

Reference the MAN page for clogin within Rancid.  Also 
leverage the -h or --help under the script.  

Author: Charles Allen
Date: 18 May 2020

Assumptions:

- 	the devices are already registered and used by Rancid 
	under router.db files.  This script does not verify 
	that the device listed in router.db is a Cisco device.

- 	if the -u flag is not used, then the login information
	must be provided under the users .cloginrc file

- 	For the global variable baseDirPath, it must be pointed
	to the base directory where the config files are store.
	In this case, it is written for /usr/local/rancid/var. 


************************************************************
'''



baseDirPath = "/usr/local/rancid/var"
cloginPath = "/usr/local/rancid/bin/clogin"


def getRouterDbList (rancid_group):

	'''
	Pull the list of devices from the group router.db file
	'''
	theGroup = rancid_group
	routerDbFile = "{}/{}/router.db".format(baseDirPath,theGroup)
	returnList = []

	if os.path.isfile(routerDbFile):
		with open(routerDbFile) as f:
			output = f.readlines()

		for line in output:
			returnList.append(line.split(';')[0])

		return returnList
	else:
		print("ERROR: The router.db file does not exist for group '{}'".format(theGroup))
		print("Exiting script....")
		sys.exit()

def singleCmd (group, single_cmd,usrname = "none",passwd = "none"):

	'''
	Subroutine used to issue a single command to a group of devices.  
	'''
	theGroupList = getRouterDbList(group)
	theCmd = single_cmd

	for i in theGroupList:
		if usrname == "none":
			command = "{} -c \"{}\" {}".format(cloginPath, theCmd, i)
		else:
			command = "{} -c \"{}\" -u {} -p {} {}".format(cloginPath, theCmd, usrname, passwd, i)

		#print (command)
		os.system(command)

def multiCmd (group, command_file,usrname = "none",passwd = "none"):

	'''
	Subroutine used to issue a group of commands to a group of devices.  
	'''
	theGroupList = getRouterDbList(group)
	cmdFile = command_file

	if not os.path.isfile(cmdFile):
		print("ERROR: The command file does not exist:'{}'".format(cmdFile))
		print("Exiting script....")
		sys.exit()

	for i in theGroupList:
		if usrname == "none":
			command = "{} -x {} {}".format(cloginPath, cmdFile, i)
		else:
			command = "{} -c \"{}\" -u {} -p {} {}".format(cloginPath, theCmd, usrname, passwd, i)
		#print (command)
		os.system(command)

def getPasswd():
	
	'''
	Subroutine used to gather the password for an alternative user.    
	'''
	verifyPass = True

	while (verifyPass):
		password1 = getpass(prompt="Enter alternative user password: ")
		password2 = getpass(prompt="Re-enter alternative user password: ")

		if (password1 != password2):
			print ("***Passwords does not match.  Please try again.")
			print ("")
		else:
			verifyPass = False

	return password1

def getUsername():

	'''
	Subroutine used to gather the alternative username.    
	'''
	verifyUser = True

	while (verifyUser):
		theUsername = input("Alternative username: ")
		theResponse = input("Proceed with username \'{}\'? (Y/N): ".format(theUsername))
		if theResponse == "Y" or theResponse == "y":
			verifyUser = False
		elif theResponse == "N" or theResponse == "n":
			continue
		else:
			print ("Not a valid response")

	return theUsername


'''
***************************************************
				Main Routine
***************************************************
'''

#Specify command line arguments
parser = argparse.ArgumentParser(description='Perform bulk changes via Rancid')
parser.add_argument("-g", "--group", type=str, required=True, help='Operation against Rancid group (i.e. access-switch)')
parser.add_argument("-c", "--command", type=str, help="Single command to execute")
parser.add_argument("-x", "--command-list", type=str, help="Specify file to execute a list of commands")
parser.add_argument("-u", "--username", action="store_true", help="Override cloginrc username.  Script will prompt for username and password")
args = parser.parse_args()


if not args.command and not args.command_list:
	print ("ERROR: No suitable command was provided -- please try again with either -c or -x flag")
	sys.exit()

if args.username:
	passUsername = getUsername()
	passPasswd = getPasswd()
else:
	passUsername = "none"
	passPasswd = "none"

if args.command:
	singleCmd(group = args.group,single_cmd = args.command,usrname = passUsername,passwd = passPasswd)
elif args.command_list:
	multiCmd(group = args.group,command_file = args.command_list,usrname = passUsername,passwd = passPasswd)