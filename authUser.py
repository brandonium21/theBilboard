from rauth import OAuth2Service

uber_api = OAuth2Service(
	client_id='_i56gtxzh6a6Xi-Cn9sTA9HuXuvC41UQ',
	client_secret='C4lOEPSh-RaBgvTH4HS-WLYIPaUy9fR_hNELrYtu',
	name='The Bilboard',
	authorize_url='https://login.uber.com/oauth/authorize',
	access_token_url='https://login.uber.com/oauth/token',
	base_url='https://api.uber.com/v1/',
 )

parameters = {
	'response_type': 'code',
	'redirect_uri': 'http://127.0.0.1:8000/users/',
	'scope': 'profile',
}

# Redirect user here to authorize your application
login_url = uber_api.get_authorize_url(**parameters)
