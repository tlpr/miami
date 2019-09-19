#!/usr/bin/python3

# The Las Pegasus Radio (https://github.com/tlpr)
# This code is licensed under the GNU GPL-3.0-only license
# https://www.gnu.org/licenses/gpl-3.0.html

import threading, asyncio, re

from disco   import miami_disco
from irc     import miami
from handler import command

# Load plugins
cmd = command()

async def irc_react(self, sender, contents):
	# IRC -> Discord
	channel_id = int(conf["BOT"]["DISCOCHAN"])
	channel = dis.get_channel(channel_id)
	contents = contents.replace("@everyone", "@everypony") # fix @everyone and
	contents = contents.replace("@here", "@there")         # @here exploit
	mentions = re.findall("\w{4,32}\#[0-9]{4}", contents)
	if mentions:
		guild = channel.guild
		for mention in mentions:
			member = guild.get_member_named(mention)
			if member == None: continue
			contents = contents.replace(mention, member.mention)
			
	asyncio.run_coroutine_threadsafe(channel.send(f"**{sender}**: {contents}"), disco_loop)
	
async def dis_react(self, message, edited=False):
	# Discord -> IRC

	# Ignore if message comes from different channel
	if not message.channel.id == int(conf["BOT"]["DISCOCHAN"]): return

	# Handle commands
	if message.content.startswith ( conf["BOT"]["CMDPREFIX"] ):
		cmd.execute(message);
		
	sender = message.author.nick if message.author.nick != None else message.author.name
	contents = message.content
	for attachment in message.attachments:
		contents += f" {attachment.url}"
	if len(contents) > 490:
		contents = contents[:487] + "..."
	contents = contents.replace("\n", " ") # remove newlines
	for mentioned_member in message.mentions:
		contents = contents.replace(mentioned_member.mention, f"@{mentioned_member.display_name}#{mentioned_member.discriminator}")
	if sender == conf["BOT"]["DISCONAME"]: return
	edited = " (edited)" if edited else ""
	irc.send_message(conf["SERVER"]["CHANNEL"], f"{sender}{edited}: {contents}")

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
