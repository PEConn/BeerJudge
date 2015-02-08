__author__ = 'michelleyeo'
from flask import Flask
import nltk
import TFIDF_thingy
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import sys
path = sys.path.append("../backend/")
import beergarage
from beergarage import ABInBev

########## Functions ###########
def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist

def topn(n, list):
    if (n > len(list)):
        return list
    else:
        return list[0:n]


# This function takes a string and extracts the keywords
def keywords(str, n, tokeniser, stop):
    # Tokenise and clean string, remove duplicates
    str = str.lower()
    tokenisedString = tokeniser.tokenize(str)
    filtered_words = [w for w in tokenisedString if not w in stop]
    uniqueFilteredWords = unique_list(filtered_words)

    # Sort and get top n words
    wordList = []
    for word in uniqueFilteredWords:
        if word in TFIDF_thingy.d:
            wordList.append((word, TFIDF_thingy.d[word]))
        else:
            wordList.append((word, 0))
    wordList.sort(key=lambda tup: tup[1], reverse=True)
    topWordList = topn(n, wordList)

    # transform into string and pass to beer API
    query = ""
    for word in topWordList:
        query += " "
        query += word[0]
    # print(query)
    return query

def getFoodVec(foodCons, foodAcc, Flavour):
    food = np.zeros(7)
    for key, val in foodCons.items():
        food[Flavour[key] - 1] = val
    for key, val in foodAcc.items():
        food[Flavour[key] - 1] = val
    return food

def getBeerVec(beer_d, Flavour):
    beer = np.zeros(7)
    for key, val in beer_d.items():
        if key in Flavour.keys():
            beer[Flavour[key] - 1] = val
        else:
            continue
    return beer

def score(food, beer):
    out = cosine_similarity(food, beer)
    return out[0][0]

# menu is a list of tuples, the first is the string of beers in the menu, the following tuples are menu food entries
def start(menu):
    # Initialising and declaring stuff
    ab = ABInBev()
    Flavour = {'green_hoppy' : 1, 'roasted_toasted' : 2, 'citrus_zesty' : 3, 'sour' : 4, 'spicy' : 5, 'fruity' : 6, 'toffee_caramel' : 7}
    TFIDF_thingy.init()

    # Get the set of English stopwords from nltk
    stop = stopwords.words('english')
    stop.extend(["sauce", "side", "served", "english", "french", "italian", "mixed", "leaves", "baked", "toasted", "fried", "cooked", "spanish", "seasonal", "w"])
    tokeniser = RegexpTokenizer(r'\w+')

    # Get the beer vector
    beerStr = menu[0]
    beerQueries = beerStr.split(' ')
    beerVecs = []
    for beerQuery in beerQueries:
        beer_d = {}
        beerDetails = ab.getBeerDetailsAsDict(beerQuery)
        if len(beerDetails['beers']) > 0:
            for beer in beerDetails['beers']:
                if beer['flavorProfile'] not in beer_d.keys():
                    beer_d[beer['flavorProfile']] = 1
                else:
                    beer_d[beer['flavorProfile']] += 1
        beer = getBeerVec(beer_d, Flavour)
        beerVecs.append(beer)

    # Get food vector for each food item, and then output result
    allres = []
    for item in menu[1:len(menu)]:
        name = item[0]
        str = name + item[1]
        foodQuery = keywords(str, 3, tokeniser, stop)

        foodDetails = ab.getIdealFlavourForFood(foodQuery)
        foodCons = foodDetails[0]
        foodAccs = foodDetails[1]

        food = getFoodVec(foodCons, foodAccs, Flavour)
        maxscore = 0
        topbeer = beerQueries[0]
        count = 0
        for beer in beerVecs:
            res = score(food, beer)
            if (res > maxscore):
                maxscore = res
                topbeer = beerQueries[count]
            else:
                topbeer = beerQueries[count]
            count += 1

        allres.append((name, topbeer, maxscore))

    topres = []
    for beer in beerQueries:
        top = sorted(filter(lambda x: x[1] == beer, allres), key=lambda x: x[2], reverse=True)
        if (len(top) > 0):
            topres.append(top[0])
    return topres


#Example:
menu = [("stella budweiser"), ("kimchi fried rice", "Fried kimchi (pickled chinese cabbage) & pork w/ steamed tofu"), ("Chicken", "Ancho-Rubbed Chicken & Chorizo Tacos")]
out = start(menu)
print(out)
