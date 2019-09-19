#!/usr/bin/python3

# The Las Pegasus Radio (https://github.com/tlpr)
# This code is licensed under the GNU GPL-3.0-only license
# https://www.gnu.org/licenses/gpl-3.0.html

from plugins.github import get_github


class command:


	def __init__ (self):
		
		self.github = get_github


	def execute (self, message):

		command_name = message.content.split(" ", 1)[0][1:]
		print(command_name)
		
		if ( command_name == "github" ):
			return self.github (message)
		

