#!/usr/bin/python
'''
Created on Nov 13, 2013

@author: tvandrun
'''

import nltk
from nltk.corpus import PlaintextCorpusReader
from nltk.corpus import wordnet as wn
from random import choice
import sys

# English stopwords
stopwords = nltk.corpus.stopwords.words('english')

# open the corpus
source_file = open(sys.argv[1], 'r')

for line in source_file :
    # modified line
    mod_line = ""

    # step through the tokens on this line
    tokens = [x.lower() for x in nltk.word_tokenize(line)]
    for word in tokens:        

        # the modified word (by default, the original word)
        mod_word = word

        # ...
        # pick a different word, possibly
        # ...

        # add the modified word to the modified line
        mod_line += " " + mod_word

    # print the modified word
    print mod_line
    
        
