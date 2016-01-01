#!/usr/local/bin/python3.4
# coding=utf-8
################################################################################################
# Name: 		BotiBot
#
# Beschreibung:	Telegram Bot BotiBot
#               Erlaubte Chat_ID's und Token müssen in configuration.json eingetragen werden
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
import sys
import os 
import logging
import subprocess 
import datetime
import time
import telegram
from telegram import Updater
from Utils import cl_utils

# Enable logging
root = logging.getLogger()
root.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = \
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)
logger = logging.getLogger(__name__)

# Instance
utils_inst = cl_utils()

# command handlers
def	start(bot, update):
	bot.sendChatAction(chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING)
	bot.sendMessage(update.message.chat_id, text='Boti wurde gestartet')
	
def	help(bot, update):
	if False == utils_inst.chatId_allowed(update.message.chat_id):
		bot.sendMessage(update.message.chat_id, text='Keine Berechtigung!')
	# TODO log not existing Users
		return
	# get help from each service	
	bot.sendMessage(update.message.chat_id, text=utils_inst.getHelpTxt())
	
	
def echo(bot, update):
	return

	
def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))		

def unknown(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="Dieser Befehl ist nicht bekannt. Bitte in /help nachschauen!")



	
def main():
	#create event handler
	updater = Updater(token = utils_inst.getToken())
	dispatcher = updater.dispatcher
	# register handlers
	dispatcher.addTelegramCommandHandler("start", start)
	dispatcher.addTelegramCommandHandler("help", help)
	# register Handlers from service files (dyn)
	for module in utils_inst.getModules():
		functions_list = utils_inst.getFunctionsList(utils_inst.getModules()[module])
		i = 0
		for func in functions_list:
			# test dyn call of func in module
			#getattr(utils_inst.getModules()[module],functions_list[i][0])()
			# handlers
			funcTXT = functions_list[i][0]
			if funcTXT == "getHelpTxt":
				utils_inst.setHelpTxt(getattr(utils_inst.getModules()[module],functions_list[i][0])())
			else:
				function = getattr(utils_inst.getModules()[module],functions_list[i][0])
				dispatcher.addTelegramCommandHandler(funcTXT,function)
			i = i + 1	

	
	
	
	#print utils_inst.getModules()
	# on noncommand
	dispatcher.addUnknownTelegramCommandHandler(unknown)
	dispatcher.addTelegramMessageHandler(echo)
	
	# Error handler
	dispatcher.addErrorHandler(error)
	
	#start BOT
	updater.start_polling(timeout=5)
	updater.idle()
	
if __name__ == '__main__':
	main()

	

