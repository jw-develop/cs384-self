'''
Created on Oct 15, 2015

Simulate a Hidden Markov Model with the given specifications

@author: tvandrun
'''

from hmm import HMM

model = HMM(["S", "M", "L"], [[0.7, 0.3],[0.4, 0.6]], [[0.1, 0.4, 0.5],[0.7, 0.2, 0.1]], 
            [0.6, 0.4])
print model.simulate(10)
