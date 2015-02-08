import sqlite3
import json
from flask import Flask, request, session, g, redirect, url_for, \
             abort, render_template, flash
from contextlib import closing
from flask_bootstrap import Bootstrap
from menuParsing.menuParsing import *
from beergarage import *
import sys
sys.path.append('../src')
import beerParser
# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
Bootstrap(app)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as  db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route("/")
def hello():
    db = get_db
    ## dbstuff = db.execcute('SELECT * FROM stuff WHERE')
    ## entries = cur.fetchall()
    return render_template('index.html')

@app.route("/beerDetails")
def beerDetails():
    return render_template('beerDetails.html')

@app.route("/beerDetails/<searchString>")
def beerSearch(searchString):
    beers = getBeerDetails(searchString)
    print beers
    return beers

@app.route("/restaurantMap")
def restaurantMap():
    return render_template('restaurantMap.html');

@app.route("/get_restaurants", methods=['GET','POST'])
# example http://0.0.0.0:5000/get_restaurants?lat=51.5152855607142&long=-0.111821715082156
def getRestaurants():
    lat = request.args.get('lat')
    long = request.args.get('long')
    try:
        rad = request.args.get('radius')
    except:
        pass
    # print lat,long
    # print
    if rad:
        ids = getRestaurantIDs((lat,long),rad)
    else:
        ids = getRestaurantIDs((lat,long))

    print lat,long
    if rad:
        print rad
    print ids
    for i in ids:
        print i['lat'],i['long']
    if ids:
        return json.dumps(ids)
    else:
        return json.dumps({'results':None})



@app.route("/choose_restaurant",methods=['GET'])
# example http://0.0.0.0:5000/choose_restaurant?id=0a868cf34ddf1f0acbbc
def choose_restaurant():
    id = request.args.get('id')
    menuList = getMenuList(id)
    beerItems = getBeerItems(menuList,v=True)
    foodItems = getFoodItems(menuList,v=True)
    menu = []
    menu.append(' '.join(beerItems))
    menu += foodItems
    for i in menu:
        print i
    r = beerParser.start(menu)
    # pair = ('becks',(u'Lamb Rogan Josh', u'Tenderly cooked off-the-bone lamb, w/ onion, tomato & pimentos, in a rich, medium sauce'))


    return json.dumps(r)
    # print printMenu(menuList)
    # Call Michelle's Code
    # return json.dumps(foodItems)
    # return render_template('beerDetails.html')

if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0',debug=True)
