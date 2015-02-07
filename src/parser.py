__author__ = 'michelleyeo'
from flask import Flask
import nltk
import cPickle
import itertools
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

########## Functions ###########
def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist

def topn(n, list):
    if (n < len(list)):
        return list
    else:
        return list[:n]

################################

# Get the set of English stopwords from nltk
stop = stopwords.words('english')
tokeniser = RegexpTokenizer(r'\w+')

# Tokenise and clean string, remove duplicates
testString = "Chicken teriyaki in peri-peri sauce, served with a side of fries"
tokenisedString = tokeniser.tokenize(testString)
for word in tokenisedString:
    word.lower()
    if word in stop:
        tokenisedString.remove(word)
unique_list(tokenisedString)

# Sort and get top n words
n = 3
wordList = []
for word in tokenisedString:
    if word in d.keys():
        wordList.append((word, d[word]))
    else:
        wordList.append((word, 0))
wordList.sort(key=lambda tup: tup[1])
topWordList = topn(n, wordList)

# Greedy search- search for all permutations of the top n words
for i in range(n):
    tupleList = itertools.permutations(topWordList, i)
    for tuple in tupleList:
        #search for thingy





