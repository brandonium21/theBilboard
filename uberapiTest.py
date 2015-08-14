import requests
import pprint

access_token = '8mUPVnck1Pk43KPcC9ndMWKstvpMxm'

url = 'https://sandbox-api.uber.com/v1/requests'
response = requests.post(
    url,
    headers={
        'Authorization': 'Bearer %s' % access_token,
        "start_latitude": "37.334381",
        "start_longitude": "-121.89432",
        "end_latitude": "37.77703",
        "end_longitude": "-122.419571",
        "product_id": "a1111c8c-c720-46c3-8534-2fcdd730040d"
    }
)
data = response.json()
pprint.pprint(data)
