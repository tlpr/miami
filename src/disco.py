#!/usr/bin/python3

# The Las Pegasus Radio (https://github.com/tlpr)
# This code is licensed under the GNU GPL-3.0-only license
# https://www.gnu.org/licenses/gpl-3.0.html

import discord, asyncio, configparser
from datetime import datetime

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

	async def on_message(self, message, edited=False):
		pass

	async def on_message_edit(self, old_message, new_message):
		if old_message.pinned: return # ignore pinned messages
		if (datetime.timestamp(old_message.created_at) + 3600) < datetime.timestamp(new_message.edited_at):
			return # do not send edited message if the original message
			       # is older than a hour.
		await self.on_message(new_message, edited=True)

