#!/usr/bin/python3

# The Las Pegasus Radio (https://github.com/tlpr)
# This code is licensed under the GNU GPL-3.0-only license
# https://www.gnu.org/licenses/gpl-3.0.html

from plugins.github import github_plugin


class command:


	def __init__ (self):
		
		github = github_plugin();
		self.github = github.execute


	def execute (self, message):

		try:
			command_name = message.content.split(" ", 1)[0][1:]
			message = message.content
		except AttributeError:
			command_name = message.split(" ", 1)[0][1:]

		if ( command_name == "github" ):
			return self.github (message)
		

