#!/usr/bin/python
# coding=utf-8
################################################################################################
# Name: 		Weather Services
#
# Beschreibung:	Project Klimamonitor is needed             
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
import time
import datetime as dt
import json
import sys
import os 
import imp
import MySQLdb as mdb
from MySQLdb import Error
import telegram
######## Helper class ##########################################################################
class clHelper():
	# Init
	def __init__(self):
		path = os.path.dirname(os.path.abspath(sys.argv[0]))
		confFile = path + "/services/wetter/conf.json"
		self.__confData = self.openConfData(confFile)
		self.__databaseName = self.__confData["databaseName"]
		self.__databaseTable = self.__confData["databaseTable"]
		self.__DBConf = self.__confData["DBConf"]
	def openConfData(self,confFile):
		with open(confFile) as data_file:    
			confData = json.load(data_file)
		return confData
	
	def getDataFromDB(self):
		try:         
			dbConnect=mdb.connect(host='127.0.0.1', db=self.__databaseName, read_default_file=self.__DBConf)
			with dbConnect:
				print('Connected to MySQL database')

				dbCursor = dbConnect.cursor()
				dbCursor.execute("SELECT forecast,trend,temperature,humidity,pressure FROM " +  self.__databaseTable + " ORDER BY timeStamp DESC LIMIT 1")
				result = dbCursor.fetchone()
				return float(result[0]), result[1], float(result[2]), float(result[3]), float(result[4])

		except Error as e:
			print(e)

		finally:
			dbConnect.close

	def getWeather(self):
		forecast, trend, temp, hum, pressure = self.getDataFromDB()
		text = "Vorhersage: " + self.getForecastText(forecast) + " " + self.getForecastIcon(forecast) + "\nTrend: " + trend + "\nLuftdruck = %.2f hPa" % pressure + "\nrel Feuchte = %.2f " % hum  + "\nTemperatur = %.2f C" % temp
		return text	
	
	def getForecastText(self,forecast):
		if forecast == 6:
			text = "sonnig"
		elif forecast == 5:
			text = "heiter"
		elif forecast == 4:
			text = "bewoelkt"
		elif forecast == 3:
			text = "bedeckt"
		elif forecast == 2:
			text = "wechselhaft"
		elif forecast == 1:
			text = "vereinzelt Regen"
		elif forecast == 0:
			text = "Regen"
		elif forecast == -1:
			text = "Gewitter"
		else:
			text ="else"
		return text
	
	def getForecastIcon(self,forecast):
		if forecast == 6:
			icon = telegram.Emoji.SUN_WITH_FACE
		elif forecast == 5:
			icon = telegram.Emoji.SUN_BEHIND_CLOUD
		elif forecast == 4:
			icon = telegram.Emoji.SUN_BEHIND_CLOUD
		elif forecast == 3:
			icon = telegram.Emoji.CLOUD
		elif forecast == 2:
			icon = telegram.Emoji.CLOUD
		elif forecast == 1:
			icon = telegram.Emoji.UMBRELLA_WITH_RAIN_DROPS
		elif forecast == 0:
			icon = telegram.Emoji.UMBRELLA_WITH_RAIN_DROPS
		elif forecast == -1:
			icon = telegram.Emoji.HIGH_VOLTAGE_SIGN
		else:
			icon ="else"
		return icon	

######## put the help text in this function ####################################################
def getHelpTxt():
	return "/wetter - Liefert aktuelle Wetterdaten \n"

######## put your services below ###############################################################
def wetter(bot, update):
	inst = clHelper()
	text = inst.getWeather()
	bot.sendMessage(update.message.chat_id, text=text)	
		