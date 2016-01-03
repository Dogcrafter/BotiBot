#!/usr/local/bin/python3.4
# coding=utf-8
################################################################################################
# Name: 		Auth Klasse
#
# Beschreibung:	Liest und prüft die Berechtigungen  
#				welche in auth.json eingetragen wurden.
#
# Version: 		1.0.0
# Author: 		Dogcrafter
# Author URI: 	https://blog.dogcrafter.de
# License: 		GPL2
# License URI: 	http://www.gnu.org/licenses/gpl-2.0.html
################################################################################################
# Changelog 
# 1.0.0 - 	Initial release
################################################################################################
import json
import sys
import os 
import imp
from inspect import getmembers, isfunction

class clAuth:
	# Init
	def __init__(self):
		path = os.path.dirname(os.path.abspath(sys.argv[0]))
		authFile = path + "/files/auth.json"
		self.__authData = self.openAuthData(authFile)
		self.__token = self.__authData["token"]
		self.__chatIds = self.__authData["allowedChatIds"]

	def openAuthData(self,authFile):
		with open(authFile) as data_file:    
			authData = json.load(data_file)
		return authData
	# Get Security Token
	def getToken(self):
		return self.__token
	# Check ChatId against approved ChatId's
	def chatId_allowed(self, chatId):
		ok_list = self.__chatIds
		if chatId in ok_list:
			result = True
		else:
			result = False
		return result
	
	