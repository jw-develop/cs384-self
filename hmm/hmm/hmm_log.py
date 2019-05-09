'''
Created on Oct 15, 2015

Implementation of a generalized Hidden Markov Model
using logarithmic arithmetic

@author: tvandrun
'''


import random
import math

infinity = float('inf')

# ---------------- Utilities ----------------


# Given a discrete distribution as a list of probabilities
# (for example, if distribution[i] = p, then i occurs with
# probability p), generate a random value, represented as
# an index into this list, based on this distribution
def find_random(distribution):
    x = random.random()
    i = 0
    s = 0.0
    while True :
        s += distribution[i]
        if x < s or i == len(distribution) - 1:
            break
        i += 1
    return i

# Given a list, find the max value and its index
def max_argmax(xx):
    # max is predefined in python :(
    maxx = xx[0]
    argmax = 0
    for i in range(1, len(xx)) :
        x = xx[i]
        if x > maxx :
            maxx = x
            argmax = i
    return (maxx, argmax)
    
# Given a list, find the index of the max value
def argmax(xx) :
    return max_argmax(xx)[1]


# -------------- for log arithmetic --------------

# assumes terms are already logs; computes the log
# of the sum of what they are logs of
def log_sum(terms):
    if len(terms) == 0 :
        return 1  # I think...
    terms.sort(reverse=True)
    try :
        return terms[0] + math.log1p(sum([math.exp(x - terms[0]) for x in terms[1:]]))
    except OverflowError :
        print "********"
        print terms
        print [x - terms[0] for x in terms[1:]]
        print [math.exp(x - terms[0]) for x in terms[1:]]
        print sum([math.exp(x - terms[0]) for x in terms[1:]])
        print math.log1p(sum([math.exp(x - terms[0]) for x in terms[1:]]))
   

# algebraically the same result as sum(), but this first
# converts all the terms to logs, then log-sums them,
# then converts the result back to non-log
def sum_log_sum(terms) :
    return math.exp(log_sum([math.log(x) for x in terms]))
    

# -------------- Class to represent a hidden Markov model  -------
# 
    
 
# Are observations known by their actual symbol or by their index?
# obs_syms is a list of actual symbols, with their canonical index
# being where that symbol is found in obs_syms

# Class to model Hidden Markov Models
class HMM :

    # Constructor take the set of observation symbols (or vocabulary),
    # and the transition, observation, and initial state probabilities (A, B, pi)
    def __init__(self, obs_syms, trans_probs, obs_probs, init_state_probs):
        self.obs_syms = obs_syms
        # "observation symbols reversed", which lets us look up the
        # index for an observation symbol.
        self.obs_syms_rev = {obs_syms[i]:i for i in range(len(obs_syms))}
        self.reset_probs(trans_probs, obs_probs, init_state_probs)

    # Reset the probability matrices (as during training)
    # This performs checks to make sure that the pi and the columns of A and B
    # are probability distributions, etc.
    def reset_probs(self, trans_probs, obs_probs, init_state_probs) :
        # Number of observation symbols
        M = len(self.obs_syms)

        # Number of states
        N = len(trans_probs)

        # Make sure the new A and B are th right size
        for row in trans_probs :
            assert len(row) == N
        assert len(obs_probs) == N
        for row in obs_probs :
            assert len(row) == M
        assert len(init_state_probs) == N       

        # Make sure the columns of A are probability distributions
        for trans_probs_i in trans_probs:
            assert math.fabs(1.0 - sum(trans_probs_i)) < .0001
        # Set the new A
        self.trans_probs = trans_probs
        # Compute the logs of A
        self.trans_probs_logs = [[math.log(trans_probs[i][j]) for j in range(len(trans_probs[i]))]
                                 for i in range(len(trans_probs))]

        # Do similarly for B
        for obs_probs_i in obs_probs :
            assert math.fabs(1.0 - sum(obs_probs_i)) < .0001
        self.obs_probs = obs_probs
        self.obs_probs_logs = [[math.log(obs_probs[i][j]) for j in range(len(obs_probs[i]))]
                                 for i in range(len(obs_probs))]


        # Hack to prevent zero probability in pi: if any state would have zero probability
        # of being the initial state, then don't update pi.
        # (This makes sene when N=2, but not for greater N)
        if all([p > 1e-300 for p in init_state_probs]) :
            # check , set, and logify pi
            assert math.fabs(1.0 - sum(init_state_probs)) < .0001
            self.init_state_probs = init_state_probs
            self.init_state_probs_logs = [math.log(pii) for pii in init_state_probs]
        
        
    # Emit a sequence of symbols by simulating a sequence of state
    # based on the probabilities of this model    
    def simulate(self, T):
        state = find_random(self.init_state_probs)
        observations = []
        while T > 0 :
            observations.append(self.obs_syms[find_random(self.obs_probs[state])])
            state = find_random(self.trans_probs[state])
            T -= 1
        return observations
    
    # Emit a sequence of symbols together with the states emitting them,
    # simulated based on the probabilities of this model
    def simulate_tagged(self, T):
        state = find_random(self.init_state_probs)
        observations = []
        while T > 0 :
            observations.append((self.obs_syms[find_random(self.obs_probs[state])], state))
            state = find_random(self.trans_probs[state])
            T -= 1
        return observations


    # The next few are so that we can refer to the parts of the model as a, b, and pi,
    # as in the formuals, and to retrieve the log values

    # Retrieve the probability of transitioning from state i to state j,
    # here for notational convenience
    def a(self, i, j):
        return self.trans_probs[i][j]

    def log_a(self, i, j) :
        return self.trans_probs_logs[i][j]
    
    # Retrieve the probability of emitting an observation symbol when in state i,
    # here for notational convenience.
    # obs can be either a symbol itself or an index into the list of symbols
    def b(self, i, obs):
        # the variable v is unused, appearing only for clarity
        if isinstance(obs, int) :
            j = obs
            v = self.obs_symbs[j]
        else :
            v = obs
            j = self.obs_syms_rev[v]
        return self.obs_probs[i][j]

    def log_b(self, i, obs) :
        if isinstance(obs, int) :
            j = obs
        else :
            j = self.obs_syms_rev[obs]
        return self.obs_probs_logs[i][j]
        

    # Retrieve the probability of starting in state i,
    # here for notational convenience.
    def pi(self, i):
        return self.init_state_probs[i]

    def log_pi(self, i) :
        return self.init_state_probs_logs[i]

    # compute the probability of an observation sequence (Problem 1; the Forward algorithm)
    def prob_observations(self, obs_seq):
        N = len(self.init_state_probs)
        T = len(obs_seq)
        alphas = self.forward_alphas(obs_seq)
        return math.exp(log_sum([alphas[T-1][i] for i in range(N)]))
 
    def forward_alphas(self, obs_seq):
        N = len(self.init_state_probs)
        T = len(obs_seq)
        alphas = [[infinity for i in range(N)] for t in range(T)]

        # compute the left column
        for i in range(N) :
            alphas[0][i] = self.log_pi(i) + self.log_b(i, obs_seq[0])

        # fill in the other columns
        for t in range(1, T) :
            o_t = obs_seq[t]
            for i in range(N) :
                alphas[t][i] = (log_sum([alphas[t-1][j] + self.log_a(j, i) for j in range(N)]) 
                                + self.log_b(i, o_t))
        return alphas
    
    # compute the probability of an observation sequence
    # (Alternate solution to Problem 1; the Backward algorithm)
    def prob_observations_alt(self, obs_seq):
        N = len(self.init_state_probs)
        T = len(obs_seq)
        betas = self.backward_betas(obs_seq)
        o_0 = obs_seq[0]
        return math.exp(log_sum([self.log_pi(i) + betas[0][i] + self.log_b(i, o_0) for i in range(N)]))

    def backward_betas(self, obs_seq):
        N = len(self.init_state_probs)
        T = len(obs_seq)
      
        #betas = [[0 for i in range(N)] for t in range(T)]
        betas = [[infinity for i in range(N)] for t in range(T)]
        
        for i in range(N) :
            #betas[T-1][i] = 1
            betas[T-1][i] = 0
        
        for t in reversed(range(T-1)) :
            o_tp = obs_seq[t+1]  # observation at time t+1
            for i in range(N) :
                #betas[t][i] = sum([self.a(i,j) * betas[t+1][j] * self.b(j, o_tp) for j in range(N)])
                betas[t][i] = log_sum([self.log_a(i,j) + betas[t+1][j] + self.log_b(j, o_tp) for j in range(N)])
                               
        
        return betas
    
    
# Class to represent an HMM that is trained by getting a training sequence and
# other parameters and using the forward-backward algorithm to train
        
class Trained_HMM(HMM):
    
    def __init__(self, train_seq, obs_syms, num_states):
        self.train_seq = train_seq
        N = num_states
        M = len(obs_syms)
        T = len(train_seq)
        # Make random initial pi, a, and b.
        # Apparently the best thing is to make them slightly off from
        # uniformly distributed
        pi = [1.0 for i in range(N)]
        for i in range(5) :
            pi[random.randint(0,N-1)] += 1
        for i in range(N) :
            pi[i] /= (N+5)
        a = [[1.0 for j in range(N)] for i in range(N)]
        for i in range(N) :
            for j in range(5) :
                a[i][random.randint(0, N-1)] += 1
            for j in range(N) :
                a[i][j] /= (N+5)
        b = [[1.0 for j in range(M)] for i in range(N)]
        for i in range(N) :
            for j in range(5) :
                b[i][random.randint(0, M-1)] += 1
            for j in range(M) :
                b[i][j] /= (M+5)

        HMM.__init__(self, obs_syms, a, b, pi)
        
        self.train()


    # Train this HMM (Forward-Backward algorithm)
    def train(self):
        N = len(self.init_state_probs)
        M = len(self.obs_syms)
        T = len(self.train_seq)

        alphas = self.forward_alphas(self.train_seq)
        old_log_likelihood = log_sum([alphas[T-1][i] for i in range(N)])
        
        print "original log like", old_log_likelihood

        epsilon = .0001
        
        while True :
            # Compute xis and gammas
            # (alphas are already computed; betas will be computed when
            #  computing xis)
            xis = self.forward_backward_xis(alphas)
            gammas = [[log_sum([xis[t][i][j] for j in range(N)])
                       for i in range(N)]
                      for t in range(T-1)]
            gamma_sums = [log_sum([gammas[t][i] for t in range(T-1)]) for i in range(N)]

            # Recompute A, B, and pi
            pi = [math.exp(gammas[0][i]) for i in range(N)]
            if 0.0 in pi :
                for i in range(len(pi)) :
                    if pi[0] == 0.0 :
                        pi[0] = 1.0 - sum(pi)
            a = [[math.exp(log_sum([xis[t][i][j] - gamma_sums[i] for t in range(T-1)]))
                  for j in range(N)]
                 for i in range(N)]
            b = [[math.exp(log_sum([gammas[t][j]- gamma_sums[j] for t in range(T-1) 
                       if self.train_seq[t] == self.obs_syms[k]]))
                  for k in range(M)]
                 for j in range(N)]
            
            self.reset_probs(a, b, pi)
            
            # recompute alphas
            alphas = self.forward_alphas(self.train_seq)

            # compute log likelihood
            new_log_likelihood = log_sum([alphas[T-1][i] for i in range(N)])

            # how much did we change?
            if new_log_likelihood - old_log_likelihood < epsilon :
                break 

            print "new log like", new_log_likelihood, (new_log_likelihood - old_log_likelihood)
            old_log_likelihood = new_log_likelihood
        

    # Compute the xis (assuming we already have the alphas; need to compute the betas)
    def forward_backward_xis(self, alphas):
        N = len(self.init_state_probs)
        T = len(self.train_seq)
        betas = self.backward_betas(self.train_seq)
        xi_numerators = [[[alphas[t][i] + self.log_a(i, j) + self.log_b(j, self.train_seq[t+1]) + betas[t+1][j] 
                           for j in range(N)] 
                          for i in range(N)] 
                         for t in range(T-1)]
        # The xi denominators are the same for every t.
        xi_denom = log_sum([log_sum([xi_numerators[0][i][j] for j in range(N)]) for i in range(N)])

        xis = [[[xi_numerators[t][i][j] - xi_denom
                 for j in range(N)] 
                for i in range(N)]
               for t in range(T-1)]
        
        return xis
