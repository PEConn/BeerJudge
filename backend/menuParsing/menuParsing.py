__author__ = 'seneda'
import locu.api as locu

backupApiID = 'd8c9db0d0d2c7458f2b4e3f46c1ce7f7815907f3'
apiID = 'e0e00a4a7de6654e343c1a281c51da129085f6ab'

def getRestaurantId(latLong,apiID=backupApiID):
    venue_client = locu.VenueApiClient(apiID)
    venues = venue_client.search(location=latLong, radius=10, category=['restaurant'], has_menu=True)
    return venues.get('objects',{'id':''})[0].get('id','')

def getRestaurantIDs(latLong,apiID=backupApiID):
    venue_client = locu.VenueApiClient(apiID)
    venues = venue_client.search(location=latLong, radius=150, category=['restaurant'], has_menu=True)
    venues = [v for v in venues.get('objects')]
    venuesLite = []
    for venue in venues:
        venuesLite.append({})
        for k,v in venue.iteritems():
            if k in ['name','id']:
                venuesLite[-1][k] = v
    return venuesLite

def getMenuList(id,apiID=backupApiID):
    venue_client = locu.VenueApiClient(apiID)
    menuList = venue_client.get_menus(id)
    return menuList

def getItems(menuList,ignoreStrings=['----'],matchStrings=[''],v=False):
    if type(menuList) != list:
        menuList = [menuList]
    items = []
    for menu in menuList:
        if v:
            print "~~~~~~~~~~~~"
            print menu['menu_name']
            print "~~~~~~~~~~~~"
        for s in menu['sections']:
            if any(word in s['section_name'].lower() for word in ignoreStrings):
                if v:
                    print "Skipped : ", s['section_name']
                continue
            elif not any(word in s['section_name'].lower() for word in matchStrings):
                if v:
                    print "Skipped : ", s['section_name']
                continue
            if v:
                print
                print '\t',s['section_name']
                print '\t',"++++++++++++"
            for subsection in s['subsections']:
                for item in subsection['contents']:
                    if item['type'] == 'ITEM':
                        if v:
                            print '\t\t',item['name']
                            print '\t\t\t',item.get('description','No Description')
                        items.append((item['name'],item.get('description','')))
    return items

def getFoodItems(menulist,v=False):
    # Returns a list of food items in the format [(name0,descriptio0n),(name1,description1)]
    return getItems(menulist,ignoreStrings=['beer','wine','drink','beverage'],v=v)

def getBeerItems(menulist,v=False,descriptions=False):
    # Returns a list of beer items in the format [(name0,descriptio0n),(name1,description1)]
    r = getItems(menulist,matchStrings=['beer'],v=v)
    if not descriptions:
        r = [i[0] for i in r]
    return r

def getMenuItems(id):
    menuList = getMenuList(id)
    foodItems = getFoodItems(menuList)
    beerItems = getBeerItems(menuList)
    return foodItems,beerItems

def printMenu(menuList):
    if type(menuList) != list:
        menuList = [menuList]

    for menu in menuList:
        print "~~~~~~~~~~~~"
        print menu['menu_name']
        print "~~~~~~~~~~~~"
        for s in menu['sections']:
            print
            print '\t',s['section_name']
            print '\t',"++++++++++++"
            for subsection in s['subsections']:
                for item in subsection['contents']:
                    if item['type'] == 'ITEM':
                        print '\t\t',item['name']
                        print '\t\t\t',item.get('description','No Description')

#
# # Example Usage
# id = getRestaurantIDs((51.5152855607142, -0.111821715082156))
# # menuList = getMenuList(id)
# # printMenu(menuList)
# print len(id)
# for i in id:
#     print id
