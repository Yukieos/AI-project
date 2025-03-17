"""
A dynamic programming agent for a stochastic task environment
"""

import random
import math
import sys


class DP_Agent(object):

    def __init__(self, states, parameters):
        self.gamma = parameters["gamma"]
        self.V0 = parameters["V0"]

        self.states = states
        self.values = {}
        self.policy = {}

        for state in states:
            self.values[state] = parameters["V0"]
            self.policy[state] = None


    def setEpsilon(self, epsilon):
        pass

    def setDiscount(self, gamma):
        self.gamma = gamma

    def setLearningRate(self, alpha):
        pass


    def choose_action(self, state, valid_actions):
        return self.policy[state]

    def update(self, state, action, reward, successor, valid_actions):
        pass


    def policy_evaluation(self, transition):
        """ Computes all values for current policy by iteration and stores them in self.values.
        Args:
            transition (Callable): Function that returns successor state and reward given a state and action.
        """
        threshold = 1e-6
        while True:
            difference = 0
            for s in self.states:
                value1 = self.values[s]
                action = self.policy[s]
                if action is None:
                    value2 = 0
                else:
                    successor, reward = transition(s, action)
                    if successor is None:
                        value2 = reward
                    else:
                        value2 = reward + self.gamma * self.values[successor]
                self.values[s] = value2
                difference = max(difference, abs(value1 - value2))
            if difference < threshold:
                break

    def policy_extraction(self, valid_actions, transition):
        """ Computes all optimal actions using value iteration and stores them in self.policy.
        Args:
            valid_actions (Callable): Function that returns a list of actions given a state.
            transition (Callable): Function that returns successor state and reward given a state and action.
        """
        for s in self.states:
            actions = valid_actions(s)
            if not actions:
                self.policy[s] = None
                continue

            optimal_action = None
            optimal_value = 0
            for a in actions:
                successor, reward = transition(s, a)
                if successor is None:
                    q_value = reward
                else:
                    q_value = reward + self.gamma * self.values[successor]

                if q_value > optimal_value:
                    optimal_value = q_value
                    optimal_action = a

            self.policy[s] = optimal_action



    def policy_iteration(self, valid_actions, transition):
        """ Runs policy iteration to learn an optimal policy. Calls policy_evaluation() and policy_extraction().
        Args:
            valid_actions (Callable): Function that returns a list of actions given a state.
            transition (Callable): Function that returns successor state and reward given a state and action.
        """
        while True:
            policy1 = dict(self.policy)
            self.policy_evaluation(transition)
            self.policy_extraction(valid_actions, transition)
            policy2 = False
            for s in self.states:
                if policy1[s] != self.policy[s]:
                    policy2 = True
                    break
                    
            if not policy2:
                break