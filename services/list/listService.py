#!/usr/bin/python
# coding=utf-8
################################################################################################
# Name: 		List Services
#
# Beschreibung:	List service - like ToDo-List, Database is needed             
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
class Helper():
	# Init
	def __init__(self):
		path = os.path.dirname(os.path.abspath(sys.argv[0]))
		confFile = path + "/services/list/conf.json"
		self.__confData = self.openConfData(confFile)
		self.__databaseName = self.__confData["databaseName"]
		self.__databaseTable = self.__confData["databaseTable"]
		self.__DBConf = self.__confData["DBConf"]
	def openConfData(self,confFile):
		try:
			with open(confFile) as data_file:    
				confData = json.load(data_file)
			return confData
		except: telegram.error.TelegramError("conf.json kann nicht geöffnet werden")
	
	def getDataFromDB(self):
		try:         
			dbConnect=mdb.connect(host='127.0.0.1', db=self.__databaseName, read_default_file=self.__DBConf)
			with dbConnect:
				print('Connected to MySQL database')

				dbCursor = dbConnect.cursor()
				dbCursor.execute("SELECT nr,entry FROM " +  self.__databaseTable + " ORDER BY nr ASC")
				result = dbCursor.fetchall()
				return result

		except Error as e:
			print(e)
		finally:
			dbConnect.close
	def getDataToDB(self,nr,entry):
		try:         
			dbConnect=mdb.connect(host='127.0.0.1', db=self.__databaseName, read_default_file=self.__DBConf)
			with dbConnect:
				print('Connected to MySQL database')
				dbCursor = dbConnect.cursor()
				dbCursor.execute("INSERT INTO " +  self.__databaseTable + " (nr, entry) VALUES (%s,%s)",(nr, entry))
				print "Wrote data to database"
		except Error as e:
			print(e)
		finally:
			dbConnect.close
	def delDataFromDB(self,nr):
		try:         
			dbConnect=mdb.connect(host='127.0.0.1', db=self.__databaseName, read_default_file=self.__DBConf)
			with dbConnect:
				print('Connected to MySQL database')
				dbCursor = dbConnect.cursor()
				dbCursor.execute("DELETE FROM " +  self.__databaseTable)
				print "Del data from database"
		except Error as e:
			print(e)
		finally:
			dbConnect.close

	def setList(self,entry):
		nr = len(self.getDataFromDB()) + 1
		self.getDataToDB(nr,entry)
		
	def getList(self):
		dbData = self.getDataFromDB()
		text= ""
		for listItem in dbData:
			text = text + str(listItem[0]) + " - " + listItem[1] + "\n"
		return text	
	def delList(self):
		nr = ""
		self.delDataFromDB(nr)
	

######## put the help text in this function ####################################################
def getHelpTxt():
	return "List Service \n/getList - Liste anzeigen \n /setList - Liste eingeben \n /delList - Liste loeschen \n"
	
######## put your services below ###############################################################
inst = Helper()
def getList(bot, update):
	text = inst.getList()
	bot.sendMessage(update.message.chat_id, text=text)	
		
def setList(bot, update):
	inst.setList(update.message.text)
	bot.sendMessage(update.message.chat_id, text="gespeichert")	

def delList(bot, update):
	inst.delList()
	bot.sendMessage(update.message.chat_id, text="Liste geloescht")	

	