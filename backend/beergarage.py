import requests
import json

token = requests.post(r'https://api.foodily.com/v1/token',
                      data={'grant_type' : 'client_credentials'},
                      auth=(r'ab-12', '2l94xQak1vQOKQVE'))
print token.json()['access_token']

r = requests.get('https://api.foodily.com/v1/recipes/b7xDe1h53',
                 headers={'Authorization': "Bearer " + token.json()['access_token']})
print r.text
