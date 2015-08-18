import requests
import pprint
import json

access_token = 'aErVa6Ztne35Yk4c9wGddDLRxPqtXI'

url = 'https://sandbox-api.uber.com/v1/requests'
parameters = {
    "start_latitude": "37.334381",
    "start_longitude": "-121.89432",
    "end_latitude": "37.77703",
    "end_longitude": "-122.419571",
    "product_id": "23a231fd-9fa8-45a7-b212-e3f9cb69873f"
}
response = requests.post(
    url,
    headers={
        'Authorization': 'Bearer %s' % access_token,
        'Content-Type': 'application/json',
    },
    data=json.dumps(parameters)
)
rdata = response.json()
pprint.pprint(rdata)
