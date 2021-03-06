__author__ = 'michelleyeo'
from flask import Flask
import nltk
import TFIDF_thingy
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import sys
path = sys.path.append("../backend")
from beergarage import *
import threading
import time

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
    Flavour = {'green_hoppy' : 1, 'roasted_toasted' : 2, 'citrus_zesty' : 3, 'sour' : 4, 'spicy' : 5, 'fruity' : 6, 'toffee_caramel' : 7}
    TFIDF_thingy.init()

    # Get the set of English stopwords from nltk
    stop = stopwords.words('english')
    stop.extend(["sauce", "side", "served", "english", "french", "italian", "mixed", "leaves", "baked", "toasted", "fried", "cooked", "spanish", "seasonal", "w"])
    tokeniser = RegexpTokenizer(r'\w+')

    # Get the beer vector
    beerStr = menu[0]
    print beerStr
    ABinBevBeers = ['Budweiser', 'Becks', 'Stella', 'Leffe', 'Hoegaarden', 'Guiness']
    for b in ABinBevBeers:
        if b not in beerStr:
            beerStr += ','+b
    # beerQueries = tokeniser.tokenize(beerStr)
    beerQueries = beerStr.split(',')
    beerDetails = {}
    threads = []

    def threadAppend(resultList,beerQuery):
        r = getBeerDetailsAsDict(beerQuery)
        print "########"
        print "########"
        print "########"
        print r.keys()
        print "########"
        print "########"
        print "########"
        resultList[beerQuery] = r

    beerVecs = {}
    beerUrls = {}
    for beerQuery in beerQueries:
        threads.append(threading.Thread(target=threadAppend,args=(beerDetails,beerQuery)))
        threads[-1].start()

    for t in threads:
        t.join()

    for k,beerDetail in beerDetails.iteritems():
        beer_d = {}
        print beerDetail.keys()
        url = ''
        if len(beerDetail['beers']) > 0:

            for beer in beerDetail['beers']:

                if beer['flavorProfile'] not in beer_d.keys():
                    beer_d[beer['flavorProfile']] = 1
                else:
                    beer_d[beer['flavorProfile']] += 1
                if not url:
                    url = beer['imageUrl']

        print "########"
        print "########"
        print "########"
        print k,beer_d
        print "########"
        print "########"
        print "########"

        beer = getBeerVec(beer_d, Flavour)
        print beer
        beerVecs[k]=beer
        beerUrls[k]=url

    # Get food vector for each food item, and then output result
    allres = []
    foodDetails = []
    threads = []

    def threadAppend(resultList,foodQuery,name):
        r = getIdealFlavourForFood(foodQuery)+(name,)
        resultList.append(r)


    for item in menu[1:min(10,len(menu))]:
        print time.time()
        name = item[0]
        str = name + item[1]
        foodQuery = keywords(str, 2, tokeniser, stop)
        threads.append(threading.Thread(target=threadAppend,args=(foodDetails,foodQuery,name)))
        threads[-1].start()

    print "YOU MADE %s THREADS"%len(threads)
    for t in threads:
        t.join()
    pairs = []
    count = 0
    for k,beerVec in beerVecs.iteritems():
        print "*%**%*%*%*%*%*%**%*"

        print beerQueries[count], beerVec
        print "*%**%*%*%*%*%*%**%*"
        maxscore = 0
        for food in foodDetails:
            foodCons = food[0]
            foodAccs = food[1]
            f = getFoodVec(foodCons, foodAccs, Flavour)
            sc = score(f, beerVec)
            # print food[2], f, sc
            if sc > maxscore:
                maxscore = sc
                topfood = food[2]
        if maxscore != 0:
            maxscore *= 100
            maxscore = int(maxscore)/2
            maxscore += 40
            maxscore = '%i'%maxscore+'%'
            pairs.append([topfood,k,maxscore,beerUrls[k]])
        count += 1

    #
    # for food in foodDetails:
    #     foodCons = food[0]
    #     foodAccs = food[1]
    #     f = getFoodVec(foodCons, foodAccs, Flavour)
    #     maxscore = 0
    #     topbeer = beerQueries[0]
    #     count = 0
    #     for beer in beerVecs:
    #         res = score(f, beer)
    #         if (res > maxscore):
    #             maxscore = res
    #             topbeer = beerQueries[count]
    #         else:
    #             topbeer = beerQueries[count]
    #         count += 1
    #     allres.append((name,topbeer,maxscore))

    #
    # topres = []
    # for beer in beerQueries:
    #     top = sorted(filter(lambda x: x[1] == beer, allres), key=lambda x: x[2], reverse=True)
    #     if (len(top) > 0):
    #         topres.append(top[0])
    # return topres
    pairs.sort(key=lambda tup: tup[2])
    pairs.reverse()
    return pairs
#Example:
#menu = [("stella, budweiser"), ("kimchi fried rice", "Fried kimchi (pickled chinese cabbage) & pork w/ steamed tofu")]
#start(menu)