'''
Created on Oct 27, 2015

@author: thomasvandrunen
'''

from hmm import Trained_HMM
import math
import sys

alphabet = 'abcdefghijklmnopqrstuvwxyz '

trained_model = Trained_HMM(observations, list(alphabet), 2)

# print the trained model's probabilities
print "pi:"
print trained_model.init_state_probs
print "a:"
print trained_model.trans_probs
print "b:"
for c in alphabet:
    print c, trained_model.b(0, c), trained_model.b(1, c)
    
