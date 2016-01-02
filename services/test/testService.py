#!/usr/local/bin/python3.4
# coding=utf-8
################################################################################################
# Name: 		Test Services - Template
#
# Beschreibung:	               
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


# put the help text in this function
def getHelpTxt():
	return "/test - Test Help \n/check - Check"

# put your services below
def test(bot, update):
	#if False == utils.chatId_allowed(update.message.chat_id):
	#	bot.sendMessage(update.message.chat_id, text='Keine Berechtigung!')
	#	return
	bot.sendMessage(update.message.chat_id, text='Test')
	
def check(bot, update):
	#if False == utils.chatId_allowed(update.message.chat_id):
	#	bot.sendMessage(update.message.chat_id, text='Keine Berechtigung!')
	#	return
	bot.sendMessage(update.message.chat_id, text='Check')

	

