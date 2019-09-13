#!/usr/bin/python3

# The Las Pegasus Radio (https://github.com/tlpr)
# This code is licensed under the GNU GPL-3.0-only license
# https://www.gnu.org/licenses/gpl-3.0.html

import socket, configparser, asyncio, ssl

class miami ():

	def __init__(self):
		self.reload_configuration_ini()
		self.irc_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if self.config["SERVER"]["SSL"]:
			self.irc_sock = ssl.wrap_socket(
				self.irc_sock,
				ssl_version=ssl.PROTOCOL_TLS,
				ciphers="DHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA:ECDHE-ECDSA-AES128-GCM-SHA256"
			)
	
	def console_out_debug(self, message, highlight=False):
		prefix = "\033[36m\033[1m[IRC]\033[0m "
		if (highlight):
			print("\n" + prefix + message, end="\n\n")
		else:
			print(prefix + message)
	
	def reload_configuration_ini(self):
		# Reads configuration.ini file and dumps its contents into a class variable.
		config_parser = configparser.ConfigParser()
		config_parser.read("configuration.ini")
		self.config = config_parser
		self.console_out_debug("Loaded configuration.ini!")
		return config_parser
	
	def set_nickname(self, new_nickname):
		# Set a new both username and nickname.
		self.irc_sock.send(bytes(
			f"USER {new_nickname} {new_nickname} {new_nickname} {new_nickname}\n", "UTF-8"
		))
		self.console_out_debug("NICK " + new_nickname)
		self.irc_sock.send( bytes(f"NICK {new_nickname}\n", "UTF-8") )

	def pong(self, quote=False):
		# Respond to PING to keep alive the connection.
		self.console_out_debug("PING PONG")
		if not quote:
			self.irc_sock.send( bytes("PONG :pingis\n", "UTF-8") )
		else:
			self.irc_sock.send( bytes(f"PONG :{quote}\n", "UTF-8") )
	
	def login(self):
		# Authenticates and sets the +B mode (Bot mode for Canternet), if required information given in the configuration.
		password = self.config["BOT"]["AUTOLOGIN"]
		if password:
			self.console_out_debug("Logging in with " + password)
			self.send_message("NickServ", f"IDENTIFY {password}")
		# set +B
		if int(self.config["BOT"]["BMODE"]):
			self.console_out_debug("MODE +B")
			self.irc_sock.send( bytes(f"MODE ${self.config['BOT']['NICKNAME']} +B\n", "UTF-8") )
	
	def send_message(self, channel, content):
		# Sends message to the given target.
		self.irc_sock.send( bytes("PRIVMSG " + channel + " :" + content + "\n", "UTF-8") )

	def connect(self):
		# Connects to the given server.
		self.console_out_debug( f"Connecting to {self.config['SERVER']['HOST']}:{self.config['SERVER']['PORT']}" )
		
		self.irc_sock.connect( (self.config["SERVER"]["HOST"], int(self.config["SERVER"]["PORT"])) )
			
		self.set_nickname( self.config["BOT"]["NICKNAME"] )
		
	async def join_specified_channel(self, channel=None):
		# Tells the bot to join a specified channel, or the one given in the configuration.
		if (channel == None): channel = self.config["SERVER"]["CHANNEL"]
		self.console_out_debug(f"Joining {channel}...")
		self.irc_sock.send( bytes("JOIN " + channel + "\n", "UTF-8") )
		
		irc_message = ""
		while (irc_message.find("End of /NAMES list.") == -1):
			
			await asyncio.sleep(2)
			
			if irc_message.find("PING :") != -1:
				quote = irc_message.split("PING :")[1]
				self.pong(quote)
				
			elif irc_message.find("/msg NickServ") != -1:
				self.console_out_debug("Account with this name on this server already exist. Attempting log in...")
				self.login()
				self.irc_sock.send( bytes("JOIN " + channel + "\n", "UTF-8") )
				
			try:
				irc_message = self.irc_sock.recv(2048).decode("UTF-8")
			except ConnectionResetError:
				print("IRC: CONNECTION RESET BY PEER")
				raise SystemExit
				
			irc_message = irc_message.strip("nr")
			
	async def main_loop(self):
		# Loop to receive information and keep the connection alive.
		try:
			while True:
				await asyncio.sleep(2)
				irc_message = self.irc_sock.recv(2048).decode("UTF-8")
				irc_message = irc_message.strip("nr")
				
				if irc_message.find("PRIVMSG") != -1:
					sender   = irc_message.split("!", 1)[0][1:]
					contents = irc_message.split("PRIVMSG", 1)[1].split(":", 1)[1]
					await self.react_on_message(sender, contents)
					
				elif irc_message.find("PING :") != -1:
					self.pong()
		except (KeyboardInterrupt, SystemExit):
			self.disconnect()
				
	def loop(self):
		asyncio.run(self.main_loop())
	
	def join_channel(self):
		asyncio.run(self.join_specified_channel())
	
	def disconnect(self):
		# Safely disconnect.
		self.console_out_debug("QUIT")
		self.irc_sock.send( bytes("QUIT \n", "UTF-8") )
	
	async def react_on_message(self, sender, contents):
		pass

