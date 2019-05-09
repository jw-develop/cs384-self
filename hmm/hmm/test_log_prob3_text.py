'''
Created on Oct 27, 2015

@author: thomasvandrunen
'''

from hmm_log import Trained_HMM
import math
import sys

alphabet = 'abcdefghijklmnopqrstuvwxyz '

source_file = open(sys.argv[1])
observations = []
for line in source_file :
    for c in line :
        if c in alphabet :
            observations.append(c)

num_states = int(sys.argv[2])

trained_model = Trained_HMM(observations, list(alphabet), num_states)

def float_down(f) :
    if f < .00001 :
        return 0.0
    else :
        return f
    

# print the trained model's probabilities
print "pi:"
print trained_model.init_state_probs
print "a:"
print trained_model.trans_probs
print "b:"
for c in alphabet:
    print("{: <5} {: <20} {: <20}".format(c, float_down(trained_model.b(0, c)), float_down(trained_model.b(1, c))))
    
