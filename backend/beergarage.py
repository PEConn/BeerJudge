import requests

class ABInBev:
    def __init__(self):
        self.authHeader = {}
        
    def getAuthHeader(self):
        token = requests.post(r'https://api.foodily.com/v1/token',
                              data={'grant_type' : 'client_credentials'},
                              auth=(r'ab-12', '2l94xQak1vQOKQVE'))
        authHeader = {'Authorization': "Bearer " + token.json()['access_token']}
        return authHeader

    def request(self, doReq):
        ret = doReq()
        if ret.status_code == 401:
            self.authHeader = self.getAuthHeader()
            ret = doReq()
        return ret

    def getBeerDetails(self, name, zone='NAZ', limit=50):
        doReq = lambda: requests.get('https://api.foodily.com/v1/beerLookup',
                            params={'name': name, 'zone': zone, 'limit': limit},
                            headers=self.authHeader)

        return self.request(doReq).text

    def getIdealFlavourForFood(self, name):
        doReq = lambda: requests.get('https://api.foodily.com/v1/beerPairings',
                                     params={'q': name}, headers=self.authHeader)
        resp = self.request(doReq).json()

        cons={}
        accs={}
        for pairing in resp['recipePairings']:
            for taste in pairing['pairings']:
                f = taste['flavor'][0]
                t = taste['type']
                if t == 'contrast':
                    if f in cons:
                        cons[f] += + 1
                    else:
                        cons[f] = 1
                else:
                    if f in accs:
                        accs[f] += + 1
                    else:
                        accs[f] = 1

        return (cons, accs)

if __name__ == "__main__":
    db = ABInBev()
    print db.getBeerDetails('Budweiser')
    print db.getIdealFlavourForFood('chicken')
