import requests
import pprint

url = 'https://api.uber.com/v1/me'

parameters = {
    'server_token': 'vFiYjoCmaF0WKZi4CbuutQehN8Wa4pga7O0Lxgj8',
    'latitude': 37.775818,
    'longitude': -122.418028,
}

response = requests.get(url, params=parameters)

data = response.json()
pprint.pprint(data)
