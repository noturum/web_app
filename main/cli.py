import requests
import json

a = requests.post('http://127.0.0.1/oauth/token', data={'username': 'nik', 'password': '2222'})

print(a.json()['access_token'])
at = a.json()['access_token']
headers = {
    f'Authorization': f'Bearer {at}',
}
a = requests.get('http://127.0.0.1/users/',headers=headers)
print(a.content)