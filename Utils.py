#!/usr/local/bin/python3.4
# coding=utf-8
################################################################################################
# Name: 		Utils Klasse
#
# Beschreibung:	Utils Klasse
#
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

class cl_utils:
	# Init
	def __init__(self):
		path = os.path.dirname(os.path.abspath(sys.argv[0]))
		confFile = path + "/files/configuration.json"
		self.__confData = self.openConfData(confFile)
		self.__token = self.__confData["token"]
		self.__chatIds = self.__confData["allowedChatIds"]
		self.__modules = self.setModules(path, self.__confData["modules"])
		self.__helpTxt = ""
	def openConfData(self,confFile):
		with open(confFile) as data_file:    
			confData = json.load(data_file)
		return confData
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
	# get Bot configuration
	def getFunctions(self):
		return self.__functions
	# get modules for import
	def getModules(self):
		return self.__modules
	def setModules(self, path, inModules):
		extModules = {}
		i = 0
		for module in inModules:
			mod = self.importFromURI(path + '/services/' + module)
			if mod is not None:
				extModules[i] = mod
				i = i + 1
		return 	extModules
		
	def importFromURI(self, uri, absl=False):
		if not absl:
			uri = os.path.normpath(os.path.join(os.path.dirname(__file__), uri))
		path, fname = os.path.split(uri)
		mname, ext = os.path.splitext(fname)
		no_ext = os.path.join(path, mname)
		#if os.path.exists(no_ext + '.pyc'):
		#	try:
		#		return imp.load_compiled(mname, no_ext + '.pyc')
		#	except:
		#		pass
		if os.path.exists(no_ext + '.py'):
			try:
				return imp.load_source(mname, no_ext + '.py')
			except:
				print 'Import Fehler' ,no_ext + '.py'
				pass
	# get function list from module
	def getFunctionsList(self,module):
		functions_list = [o for o in getmembers(module) if isfunction(o[1])]
		return functions_list
	# get Help text
	def getHelpTxt(self):
		return self.__helpTxt
	# set Help Text
	def setHelpTxt(self,text):
		self.__helpTxt = self.__helpTxt + text 
	def addCommandHandlerFromModules(self,dispatcher):
		for module in self.__modules:
			functions_list = self.getFunctionsList(self.__modules[module])
			i = 0
			for func in functions_list:
				# handlers
				functionText = functions_list[i][0]
				if functionText == "getHelpTxt":
					self.setHelpTxt(getattr(self.__modules[module],functions_list[i][0])())
				else:
					function = getattr(self.__modules[module],functions_list[i][0])
				dispatcher.addTelegramCommandHandler(functionText,function)
				i = i + 1	
	