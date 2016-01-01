#!/usr/local/bin/python3.4
# coding=utf-8
################################################################################################
# Name: 		Test Services
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
import time
import sys
import os
import datetime as dt

def test(bot, update):
	bot.sendMessage(update.message.chat_id, text='TEST Help')
	return
	

