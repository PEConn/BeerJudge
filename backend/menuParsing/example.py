__author__ = 'seneda'
from menuParsing import *
count = 0

cities = ["Bath ", ]#"Birmingham ", "Bradford ", "Brighton & Hove ", "Bristol ", "Cambridge ", "Canterbury ", "Carlisle ",
          # "Chelmsford ", "Chester ", "Chichester ", "Coventry ", "Derby ", "Durham ", "Ely ", "Exeter ", "Gloucester ",
          # "Hereford ", "Kingston upon Hull ", "Lancaster ", "Leeds ", "Leicester ", "Lichfield ", "Lincoln ", "Liverpool",
          # "City of London ", "Manchester ", "Newcastle upon Tyne ", "Norwich ", "Nottingham ", "Oxford ", "Peterborough ",
          # "Plymouth ", "Portsmouth ", "Preston ", "Ripon ", "Salford ", "Salisbury", "Sheffield ", "Southampton ", "St Albans",
          # "Stoke-on-Trent ", "Sunderland ", "Truro ", "Wakefield ", "Wells ", "Westminster ", "Winchester ", "Wolverhampton ",
          # "Worcester ", "York ", "Scottish Cities", "Aberdeen", "Dundee", "Edinburgh", "Glasgow", "Inverness", "Perth",
          # "Stirling", "Welsh Cities", "Bangor ", "Cardiff", "Newport ", "St Asaph", "St David's ", "Swansea", "Northern Irish Cities",
          # "Armagh", "Belfast", "Londonderry", "Lisburn", "Newry"]

ids = {'Zizzi':'129efe440a449cc1cf2c','Nandos':'88a9b45c27ca0853513f'}
for city in cities:
    venues = venue_client.search(locality = 'London', category=['restaurant'], has_menu=True)
    count += len(venues['objects'])
    for i in venues['objects']:
        ids[i['name']]=i['id']
    for restaurant,id in ids.iteritems():
        menuList = getMenuList(id)
        # print
        # print
        # print restaurant
        # print
        # print
        for i in getFoodItems(menuList):
            print i
        # print '\n\n\n\n'
        # for i in getBeerItems(menuList):
        #     print i

# print count