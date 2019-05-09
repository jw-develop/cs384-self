'''
Created on Oct 26, 2015

@author: thomasvandrunen
'''

from hmm import *
import math

model = HMM(["S", "M", "L"], [[0.7, 0.3],[0.4, 0.6]], [[0.1, 0.4, 0.5],[0.7, 0.2, 0.1]], 
            [0.6, 0.4])

print "simulated models:"

for x in range(5):
    observations = model.simulate(10)
    prob = model.prob_observations(observations)
    perplexity = math.pow(prob, - (1.0/10))
    print "forward: ", prob, perplexity
    prob = model.prob_observations_alt(observations)
    perplexity = math.pow(prob, - (1.0/10))
    print "backward: ", prob, perplexity

print "manufactured likely observation:"
prob =  model.prob_observations(['L', 'L', 'L', 'L', 'L', 'L','L','L','L','L'])
perplexity = math.pow(prob, - (1.0/10))
print "forward:", prob, perplexity
prob =  model.prob_observations_alt(['L', 'L', 'L', 'L', 'L', 'L','L','L','L','L'])
perplexity = math.pow(prob, - (1.0/10))
print "backward:", prob, perplexity
    
print "manufactured unlikely observation:"
prob = model.prob_observations(['S', 'L', 'S', 'L', 'S', 'L','S','L','S','L'])
perplexity = math.pow(prob, - (1.0/10))
print "forward:", prob, perplexity
prob = model.prob_observations(['S', 'L', 'S', 'L', 'S', 'L','S','L','S','L'])
perplexity = math.pow(prob, - (1.0/10))
print "backward:", prob, perplexity
