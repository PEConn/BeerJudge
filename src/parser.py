__author__ = 'michelleyeo'
from flask import Flask
import nltk
import math
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

########## Functions ###########
def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist
################################

# Get the set of English stopwords from nltk
stop = stopwords.words('english')
tokeniser = RegexpTokenizer(r'\w+')

# Tokenise and clean string
testString = "Chicken teriyaki in peri-peri- sauce, served with a side of fries"
tokenisedString = unique_list(tokeniser.tokenize(testString))
for word in tokenisedString:
    if word not in stop:
        print(word.lower())

# Get top words



