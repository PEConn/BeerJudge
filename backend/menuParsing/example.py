__author__ = 'seneda'
from menuParsing import *

ids = {'Zizzi':'129efe440a449cc1cf2c','Nandos':'88a9b45c27ca0853513f'}

for restaurant,id in ids.iteritems():
    menuList = getMenuList(id)
    print
    print
    print restaurant
    print
    print
    for i in getFoodItems(menuList):
        print i
    print '\n\n\n\n'
    for i in getBeerItems(menuList):
        print i