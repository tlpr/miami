#!/usr/bin/python3

# The Las Pegasus Radio (https://github.com/tlpr)
# This code is licensed under the GNU GPL-3.0-only license
# https://www.gnu.org/licenses/gpl-3.0.html

import discord, asyncio, configparser

class miami_disco (discord.Client):
	
	def console_out_debug(self, message, highlight=False):
		prefix = "\033[33m\033[1m[Discord]\033[0m "
		if (highlight):
			print("\n" + prefix + message, end="\n\n")
		else:
			print(prefix + message)
	
	def reload_configuration_ini(self):
		config_parser = configparser.ConfigParser()
		config_parser.read("configuration.ini")
		self.configini = config_parser
	
	def start_disco(self):
		try:
			self.run(self.configini["BOT"]["DITOKEN"])
		except discord.errors.LoginFailure:
			self.console_out_debug("Incorrect DITOKEN.", True)
	
	async def on_ready(self):
		self.console_out_debug("Logged in.")

