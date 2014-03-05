# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.6, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        # a= self.mdp.getStates();
        #b= self.mdp.getPossibleActions(a[1]);
        #print self.mdp.getTransitionStatesAndProbs(a[1],b[2]);
        "*** YOUR CODE HERE ***"
        i=iterations;
        
        while i>0:
            new_counter=util.Counter();
            for s in self.mdp.getStates():
                max_value = float('-inf')

                for a in self.mdp.getPossibleActions(s):
                    cur_sum=0
                    transition_states=self.mdp.getTransitionStatesAndProbs(s,a)
                    for ts in transition_states:
                        probability=ts[1]
                        ns=ts[0]
                        #ts is a tuple of next state and probability
                        cur_sum+=probability*(self.mdp.getReward(s,a,ns)+(self.discount*self.getValue(ns)))
                    if max_value<=cur_sum:
                        max_value=cur_sum
                        new_counter[s]=max_value
            self.values=new_counter
            i-=1
                            
                            

    


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        #Expected util. starting out having taken action a from s and thereafter acting optimally

        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        q=0
        transition_states=self.mdp.getTransitionStatesAndProbs(state,action)
        for ts in transition_states:
            probability=ts[1]
            ns=ts[0]
            q+=(probability*(self.mdp.getReward(state,action,ns)+self.discount*self.getValue(ns)))

        return q
        
        # util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        max_q=-99999999
        best_action=None
        for action in self.mdp.getPossibleActions(state):
                calculatedQ=self.computeQValueFromValues(state,action)
                if calculatedQ>max_q:
                    max_q=calculatedQ
                    best_action=action
        return best_action
        #util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
