#!/usr/bin/python3

# The Las Pegasus Radio (https://github.com/tlpr)
# This code is licensed under the GNU GPL-3.0-only license
# https://www.gnu.org/licenses/gpl-3.0.html

import threading, asyncio

from disco import miami_disco
from irc   import miami

async def irc_react(self, sender, contents):
	# IRC -> Discord
	channel_id = int(conf["BOT"]["DISCOCHAN"])
	channel = dis.get_channel(channel_id)
	asyncio.run_coroutine_threadsafe(channel.send(f"{sender}: {contents}"), disco_loop)
	
async def dis_react(self, message):
	# Discord -> IRC
	sender = message.author.nick if message.author.nick != None else message.author.name 
	contents = message.content
	if sender == conf["BOT"]["DISCONAME"]:
		return
	irc.send_message(conf["SERVER"]["CHANNEL"], f"{sender}: {contents}")

miami.react_on_message = irc_react
miami_disco.on_message = dis_react

global disco_loop
disco_loop = asyncio.new_event_loop()
irc = miami()
dis = miami_disco(loop=disco_loop)

global conf
conf = irc.reload_configuration_ini()
dis.reload_configuration_ini()

irc.connect()
irc.join_channel()

irc_thread = threading.Thread(target=irc.loop, name="IRC", args=())

irc_thread.start()
dis.start_disco()
