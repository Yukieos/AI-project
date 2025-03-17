"""
A Q-learning agent for a stochastic task environment
"""

import random
import math
import sys


class RL_Agent(object):

    def __init__(self, states, valid_actions, parameters):
        self.alpha = parameters["alpha"]
        self.epsilon = parameters["epsilon"]
        self.gamma = parameters["gamma"]
        self.Q0 = parameters["Q0"]

        self.states = states
        self.Qvalues = {}
        for state in states:
            for action in valid_actions(state):
                self.Qvalues[(state, action)] = parameters["Q0"]


    def setEpsilon(self, epsilon):
        self.epsilon = epsilon

    def setDiscount(self, gamma):
        self.gamma = gamma

    def setLearningRate(self, alpha):
        self.alpha = alpha


    def choose_action(self, state, valid_actions):
        """ Choose an action using epsilon-greedy selection.

        Args:
            state (tuple): Current robot state.
            valid_actions (list): A list of possible actions.
        Returns:
            action (string): Action chosen from valid_actions.
        """
        actions = valid_actions
        if not actions:
            return None
        if random.random() < self.epsilon:
            return random.choice(actions)
        else:
            max_value = 0
            optimal_actions = []
            for a in actions:
                if (state, a) in self.Qvalues:
                    q = self.Qvalues[(state, a)]
                else:
                    q = self.Q0
                if q > max_value:
                    max_value = q
                    optimal_actions = [a]
                elif q == max_value:
                    optimal_actions.append(a)
            if not optimal_actions:
                return None
            return random.choice(optimal_actions)


    def update(self, state, action, reward, successor, valid_actions):
        """ Update self.Qvalues for (state, action) given reward and successor.

        Args:
            state (tuple): Current robot state.
            action (string): Action taken at state.
            reward (float): Reward given for transition.
            successor (tuple): Successor state.
            valid_actions (list): A list of possible actions at successor state.
        """
        if (state, action) in self.Qvalues:
            current_q = self.Qvalues[(state, action)]
        else:
            current_q = self.Q0
        if successor is None:
            target = reward
        else:
            actions = valid_actions
            if not actions:
                max2 = 0
            else:
                max2 = 0
                for a in actions:
                    if (successor, a) in self.Qvalues:
                        q = self.Qvalues[(successor, a)]
                    else:
                        q = self.Q0
                    if q > max2:
                        max2 = q
            target = reward + self.gamma * max2

        self.Qvalues[(state, action)] = current_q + self.alpha * (target - current_q)