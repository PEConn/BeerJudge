import requests

class ABInBev:
    def __init__(self):
        self.authHeader = self.getAuthHeader()
        
    def getAuthHeader(self):
        token = requests.post(r'https://api.foodily.com/v1/token',
                              data={'grant_type' : 'client_credentials'},
                              auth=(r'ab-12', '2l94xQak1vQOKQVE'))
        authHeader = {'Authorization': "Bearer " + token.json()['access_token']}
        return authHeader


    def getBeerDetails(self, name, zone='NAZ', limit=50):
        beer = requests.get('https://api.foodily.com/v1/beerLookup',
                            params={'name': name, 'zone': zone, 'limit': limit},
                            headers=self.authHeader)

        if beer.status_code == 401:
            self.authHeader = getAuthHeader()
            beer = requests.get('https://api.foodily.com/v1/beerLookup',
                                params={'name': name, 'zone': zone, 'limit': limit},
                                headers=self.authHeader)

        return beer.json()
