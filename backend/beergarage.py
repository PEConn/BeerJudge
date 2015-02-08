import requests
import time

def getAuthHeader():
    token = requests.post(r'https://api.foodily.com/v1/token',
                          data={'grant_type' : 'client_credentials'},
                          auth=(r'ab-12', r'2l94xQak1vQOKQVE'))
    authHeader = {'Authorization': "Bearer " + token.json()['access_token']}
    return authHeader

authHeader = getAuthHeader()

def getBeerDetails(name, zone='EUR', limit=50):
    return requests.get('https://api.foodily.com/v1/beerLookup',
                        params={'name': name, 'zone': zone, 'limit': limit},
                        headers=authHeader).text

def getBeerDetailsAsDict(name, zone='EUR'):
    return requests.get('https://api.foodily.com/v1/beerLookup',
                    params={'name': name, 'zone': zone},
                        headers=authHeader).json()

def getIdealFlavourForFood(name):
    resp = requests.get('https://api.foodily.com/v1/beerPairings',
                                 params={'q': name}, headers=authHeader).json()

    cons={}
    accs={}

    if resp:
        for pairing in resp['recipePairings']:
            for taste in pairing['pairings']:
                f = taste['flavor'][0]
                t = taste['type']
                if t == 'contrast':
                    if f in cons:
                        cons[f] += 1
                    else:
                        cons[f] = 1
                else:
                    if f in accs:
                        accs[f] += 1
                    else:
                        accs[f] = 1
    print cons,accs
    return (cons, accs)

if __name__ == "__main__":
    db = ABInBev()
    print db.getBeerDetails('Budweiser')
    print db.getIdealFlavourForFood('chicken')
