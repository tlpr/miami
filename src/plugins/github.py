
from requests import get

class get_github:

	def __init__ (self, message):
		
		argument = message.content.split()[1]
		github_api_url = "https://api.github.com/repos/" + argument + "/commits"
		print(github_api_url)

		response = get (github_api_url).json()
		print(response)
		response = response[0]

		message = "Repository: {}\nLatest commit hash: {}\nAuthor: {} ({})\nDescription: {}"
		message = message.format( argument, str(response['sha']), response['commit']['author']['name'], response['commit']['author']['email'], response['commit']['message'] )

		return message

