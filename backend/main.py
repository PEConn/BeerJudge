import sqlite3
import json
from beergarage import ABInBev
from flask import Flask, request, session, g, redirect, url_for, \
             abort, render_template, flash
from contextlib import closing
from flask_bootstrap import Bootstrap
from menuParsing.menuParsing import *

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
    db = ABInBev()
    beers = db.getBeerDetails(searchString)
    print beers
    return beers

@app.route("/get_restaurants", methods=['GET','POST'])
def getRestaurants():

    lat = request.args.get('lat')
    long = request.args.get('long')
    print lat,long
    print
    ids = getRestaurantIDs((lat,long))
    if ids:
        return json.dumps(ids)
    else:
        return json.dumps({'results':None})

if __name__ == "__main__":
    init_db()
    app.run(host='0.0.0.0',debug=True)
