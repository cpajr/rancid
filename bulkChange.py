#!/usr/bin/env python3

import json
import requests
import argparse
import os.path
import sys
from getpass import getpass

baseDirPath = "/usr/local/rancid/var"
cloginPath = "/usr/local/rancid/bin/clogin"


def getRouterDbList (rancid_group):

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

	theGroupList = getRouterDbList(group)
	theCmd = single_cmd

	for i in theGroupList:
		if usrname == "none":
			command = "{} -c \"{}\" {}".format(cloginPath, theCmd, i)

		os.system(command)

def multiCmd (group, command_file,usrname = "none",passwd = "none"):

	theGroupList = getRouterDbList(group)
	cmdFile = command_file

	if not os.path.isfile(cmdFile):
		print("ERROR: The command file does not exist:'{}'".format(cmdFile))
		print("Exiting script....")
		sys.exit()

	for i in theGroupList:
		command = "{} -x {} {}".format(cloginPath, cmdFile, i)
		print (command)
		os.system(command)

def getPasswd():
	verifyPass = True

	while (verifyPass):
		password1 = getpass(prompt="Enter alternative user password: ")
		password2 = getpass(prompt="Re-enter alternative user password: ")

		if (password1 != password2):
			print ("***Passwords does not match.  Please try again.")
			print ("")
		else:
			verifyPass = False

	#return password
	return password1

def getUsername():

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

if args.username:
	getUsername()
	getPasswd()

# if args.command:
# 	singleCmd(group = args.group,single_cmd = args.command)
# elif args.command_list:
# 	multiCmd(group = args.group,command_file = args.command_list)
# else:
# 	print ("ERROR: No suitable argument was provided -- please try again.")