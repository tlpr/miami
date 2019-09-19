
from requests import get

class github_plugin:

	def execute (self, message):
		
		argument = message.split()[1]
		github_api_url = "https://api.github.com/repos/" + argument + "/commits"

		response = get (github_api_url).json()
		response = response[0]

		message = "Repository: {}\nLatest commit hash: {}\nAuthor: {} ({})\nDescription: {}"
		message = message.format( argument, str(response['sha']), response['commit']['author']['name'], response['commit']['author']['email'], response['commit']['message'] )

		return message

