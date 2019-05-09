'''
Created on Oct 22, 2015

@author: tvandrun
'''

from hmm import *

model = HMM(["S", "M", "L"], [[0.7, 0.3],[0.4, 0.6]], [[0.1, 0.4, 0.5],[0.7, 0.2, 0.1]], 
            [0.6, 0.4])

observationses = [model.simulate_tagged(50) for i in range(100)]

remade_model = MLE_HMM_from_known_states(["S", "M", "L"], 2, observationses)

print remade_model.obs_syms
print remade_model.trans_probs
print remade_model.obs_probs
print remade_model.init_state_probs
