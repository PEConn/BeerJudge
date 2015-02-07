__author__ = 'seneda'
import locu.api as locu

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
    return getItems(menulist,ignoreStrings=['beer','wine','drink','beverages'],v=v)

def getBeerItems(menulist,v=False):
    # Returns a list of beer items in the format [(name0,descriptio0n),(name1,description1)]
    return getItems(menulist,matchStrings=['beer'],v=v)

def getMenuList(id,apiID='e0e00a4a7de6654e343c1a281c51da129085f6ab'):
    venue_client = locu.VenueApiClient(apiID)
    menuList = venue_client.get_menus(id)
    return menuList

def getMenuItems(id):
    menuList = getMenuList(id)
    foodItems = getFoodItems(menuList)
    beerItems = getBeerItems(menuList)
    return foodItems,beerItems