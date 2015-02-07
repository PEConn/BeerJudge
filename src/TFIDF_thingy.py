__author__ = 'michelleyeo'
from flask import Flask
import nltk
import math
try:
   import cPickle as pickle
except:
   import pickle
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

# Get the set of English stopwords from nltk
stop = stopwords.words('english')
tokeniser = RegexpTokenizer(r'\w+')

########## Functions ###########
def stem(str):
    tok = tokeniser.tokenize(str)
    for word in tok:
        if word in stop:
            tok.remove(word)
    return tok

def wc(str, dict):
    tok = stem(str)
    for word in tok:
        word = word.lower()
        if word not in dict.keys():
            dict[word] = 1
        else:
            dict[word] += 1

################################
dict = {}

#str = "1 chicken wing"
#out = stem(str)
#print(len(out))







#print(dict["chicken"])

