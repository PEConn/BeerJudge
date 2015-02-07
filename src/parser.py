__author__ = 'michelleyeo'
from flask import Flask
import nltk
import TFIDF_thingy
import numpy.linalg
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

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

def keywords(str, n):
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

    print(query)

def score(food_d, beer_d)
    food = np.zeros(7)
    beer = np.zeros(7)
    for key, val in food_d.items():
        food[Flavour[key] - 1] = val

    for key, val in beer_d.items():
        beer[Flavour[key] - 1] = val

    #normalise and dot product
    score = cosine_similarity(food, beer)
    return score

################################
Flavour = {'green_hoppy' : 1, 'roasted_toasted' : 2, 'citrus_zesty' : 3, 'sour' : 4, 'spicy' : 5, 'fruity' : 6, 'toffee_caramel' : 7}
TFIDF_thingy.init()

# Get the set of English stopwords from nltk
stop = stopwords.words('english')
stop.extend(["sauce", "side", "served", "english", "french", "italian", "mixed", "leaves", "baked", "toasted", "fried", "cooked", "spanish", "seasonal", "w"])
tokeniser = RegexpTokenizer(r'\w+')

# Tokenise and clean string, remove duplicates
#name = info[0]
#str = name + info[1]
#price = info[2]
testString = "Fried kimchi (pickled chinese cabbage) & pork w/ steamed tofu"
keywords(testString, 3)
#score(name, beerlist, price)


# Dictionary of flavour to cardinality retrieved
food_d={'sour' : 46, 'toffee_caramel' : 2}
beer_d = {'sour' : 1, 'fruity' : 2, 'spicy' : 1}

food = np.zeros(7)
beer = np.zeros(7)

for key, val in food_d.items():
    food[Flavour[key] - 1] = val

for key, val in beer_d.items():
    beer[Flavour[key] - 1] = val

#normalise and dot product
score = cosine_similarity(food, beer)
print(score)






