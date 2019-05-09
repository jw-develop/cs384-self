#!/usr/bin/python
'''
Created on Sep 18, 2013

@author: tvandrun
'''

from nltk import FreqDist
import re
import math

vocab = set(w.lower() for w in file("/usr/share/dict/words").read().splitlines())
V = len(vocab)




class LanguageModelData:
    
    def __init__(self, text):
        self.fd_unigrams = FreqDist(text)
        self.fd_bigrams = FreqDist([tuple(text[i:i+2]) for i in range(len(text) - 1)])
        self.fd_trigrams = FreqDist([tuple(text[i:i+3]) for i in range(len(text) - 2)])
        self.N = len(text)
        self.count_of_counts = FreqDist([self.fd_unigrams[w] for w in vocab])

    def unigram_count(self, w):
        return float(self.fd_unigrams[w])
    
    def bigram_count(self, w1, w2):
        return float(self.fd_bigrams[(w1, w2)])
        
    def trigram_count(self, w1, w2, w3):
        return float(self.fd_trigrams[(w1, w2, w3)])



file_name = "training.txt"
raw_words = re.findall(r'[a-z][a-z\']*|\d+|[!$%*()\-:;\"\',.?]', file(file_name).read().lower())
held_out_file_name = "heldout-small.txt"
held_out_raw_words = re.findall(r'[a-z][a-z\']*|\d+|[!$%*()\-:;\"\',.?]', file(held_out_file_name).read().lower())

alphabet = "abcdefghijklmnopqrstuvwxyz'"

def transform(w):
    if w.isdigit():
        return "NUM"    
    elif all(c in alphabet for c in w) :
        if w in vocab :
            return w
        else :
            return "OOV"
    else :
        return  "PNCT"

lm_data = LanguageModelData([transform(w) for w in raw_words])        
count_of_counts = FreqDist([lm_data.fd_unigrams[w] for w in vocab])

held_out_text = [transform(w) for w in held_out_raw_words]

class ConstantLanguageModel :
    
    def p(self, w, h):
        return 1 / float(V)
    
    def kind_of_model(self):
        return "constant"

class UnigramLanguageModel :
    
    def __init__(self, lm_data):
        self.lm_data = lm_data
        
    def p(self, w, h):
        return float(self.lm_data.fd_unigrams[w]) / self.lm_data.N
    
    def kind_of_model(self):
        return "unigram"

class UnigramLaplaceLanguageModel :
    
    def __init__(self, lm_data):
        self.lm_data = lm_data
        
    def p(self, w, h):
        return float(self.lm_data.fd_unigrams[w] + 1) / (self.lm_data.N + V)
    
    def kind_of_model(self):
        return "unigram with laplace smoothing"
    
class BigramLanguageModel :
    
    def __init__(self, lm_data):
        self.lm_data = lm_data
        
    def p(self, w, h):
        try :
            if len(h) == 0 :
                return float(self.lm_data.fd_unigrams[w]) / self.lm_data.N
            else :
                return float(self.lm_data.fd_bigrams[(h[-1], w)]) / self.lm_data.fd_unigrams[h[-1]]
        except ZeroDivisionError :
            return 0.0

    def kind_of_model(self):
        return "bigram"
        
class BigramLaplaceLanguageModel :
    
    def __init__(self, lm_data):
        self.lm_data = lm_data
        
    def p(self, w, h):
        if len(h) == 0 :
            return float(self.lm_data.fd_unigrams[w]) / self.lm_data.N
        else :
            return float(self.lm_data.fd_bigrams[(h[-1], w)] + 1) / (self.lm_data.fd_unigrams[h[-1]] + V)
                
    def kind_of_model(self):
        return "bigram with Laplace smoothing"
        
        
class TrigramLanguageModel :
   
    def __init__(self, lm_data):
        self.lm_data = lm_data
        
    def p(self, w, h):
        try :
            if len(h) == 0 :
                return float(self.lm_data.fd_unigrams[w]) / self.lm_data.N
            elif len(h) == 1 :
                return float(self.lm_data.fd_bigrams[(h[0], w)]) / self.lm_data.fd_unigrams[h[-1]]
            else :
                return float(self.lm_data.fd_trigrams[(h[-2], h[-1], w)]) / self.lm_data.fd_bigrams[(h[-2], h[-1])]
        except ZeroDivisionError :
            return 0.0

    def kind_of_model(self):
        return "trigram"


class TrigramLaplaceLanguageModel :
    
    def __init__(self, lm_data):
        self.lm_data = lm_data
        
    def p(self, w, h):
        if len(h) == 0 :
            return float(self.lm_data.fd_unigrams[w]) / self.lm_data.N
        elif len(h) == 1 :
            return float(self.lm_data.fd_bigrams[(h[0], w)] + 1) / (self.lm_data.fd_unigrams[h[-1]] + V)
        else :
            return float(self.lm_data.fd_trigrams[(h[-2], h[-1], w)] + 1) / (self.lm_data.fd_bigrams[(h[-2], h[-1])] + V)

    def kind_of_model(self):
        return "trigram with Laplace smoothing"


    
class InterpolatedLanguageModel :
    
    def __init__(self, lang_mods):
        self.lang_mods = lang_mods
        self.weights = [1.0 / len(lang_mods) for lm in lang_mods]
        # you need to implement the algorithm for finding optimal weights
                
        
    def p(self, w, h):
        return sum([weight * lang_mod.p(w, h) 
                   for weight, lang_mod in zip(self.weights, self.lang_mods)])

    def kind_of_model(self):
        return "Interpolated: %s"  % " + ".join(["%s*%s"% (weight, lang_mod.kind_of_model())  
                                                for (weight, lang_mod) in zip(self.weights, self.lang_mods)])
