import os
import json
import requests

## Variables

client_id = <write service account name>
client_secret = <write service account secret id>
service = <write deployed to cluster service name>
realm = <write your Keycloak realm name>
keyloack_url = <write your Keycloak url>
cluster_url = <write cluster url when service was deployed>

route_service_url = <write route url of deployed service>
#example: f'{cluster_url}/api/v1/namespaces/{namespace}/deployments/{name}/{service_name}/default-route'>

post_request_url = <write POST url for the deployed service>
#example: f'{cluster_url}/service/{service_name}/api/{service}/invoke'>


payload = {
    "columns": [ <input data>, <input data>],
    "data": [[ <input data>, <input data> ]]
}

token_get_url = '{keyloack_url}/auth/realms/{realm}/protocol/openid-connect/token'

## Requests

id_token = requests.post(
    url=token_get_url,
    data={
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'openid',
    }
).json()['id_token']

url = requests.get(
    url=route_service_url,
    headers={
        'Authorization': f'Bearer {id_token}',
    }
).json()['status']['edgeUrl']

response = requests.post(
    url=post_request_url,
    json=payload,
    headers={
        'Authorization': f'Bearer {id_token}',
        'Content-Type': 'application/json',
})

if response.status_code == 200:
    result = json.loads(response.content.decode("utf-8"))
    print(result)
