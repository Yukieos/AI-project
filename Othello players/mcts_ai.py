#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""
MCTS AI player for Othello.
"""

import random
import numpy as np
from six.moves import input
from othello_shared import get_possible_moves, play_move, compute_utility


class Node:
    def __init__(self, state, player, parent, children, v=0, N=0):
        self.state = state
        self.player = player
        self.parent = parent
        self.children = children
        self.value = v
        self.N = N

    def get_child(self, state):
        for c in self.children:
            if (state == c.state).all():
                return c
        return None


def select(root, alpha):
    """ Starting from given node, find a terminal node or node with unexpanded children.
    If all children of a node are in tree, move to the one with the highest UCT value.

    Args:
        root (Node): MCTS tree root node
        alpha (float): Weight of exploration term in UCT

    Returns:
        node (Node): Node at bottom of MCTS tree
    """
    current = root
    while True:
        new_move = get_possible_moves(current.state, current.player)
        if not new_move:
            break
        notexpanded = False
        for n in new_move:
            new_state = play_move(current.state, current.player, n[0], n[1])
            if current.get_child(new_state) is None:
                notexpanded = True
                break
        if notexpanded:
            break
            
        highest_uct = -float("inf")
        highest_child = None
        for n in current.children:
            uct =  n.value / n.N + (alpha * np.sqrt(np.log(current.N) / n.N))
            if uct > highest_uct:
                highest_uct = uct
                highest_child = n
        current = highest_child

    root = current
    return root


def expand(node):
    """ Add a child node of state into the tree if it's not terminal.

    Args:
        node (Node): Node to expand

    Returns:
        leaf (Node): Newly created node (or given Node if already leaf)
    """
    possible_moves = get_possible_moves(node.state, node.player)
    if not possible_moves:
        return node
    
    for n in possible_moves:
        new_state = play_move(node.state, node.player, n[0], n[1])
        if node.get_child(new_state) is None:
            if node.player ==2:
                next_player = 1
            else:
                next_player = 2
            child_list = []
            leaf_node = Node(new_state, next_player, node, child_list)
            node.children.append(leaf_node)
            return leaf_node  
    return node


def simulate(node):
    """ Run one game rollout using from state to a terminal state.
    Use random playout policy.

    Args:
        node (Node): Leaf node from which to start rollout.

    Returns:
        utility (int): Utility of final state
    """
    state1 = np.array(node.state)
    player1 = node.player
    while True:
        possible_moves = get_possible_moves(state1, player1)
        if not possible_moves:
            break
        next_move = random.choice(possible_moves)
        state1 = play_move(state1, player1, next_move[0], next_move[1])
        if player1 ==2:
            player1=1
        else:
            player1=2
    return compute_utility(state1)


def backprop(node, utility):
    """ Backpropagate result from state up to the root.
    Every node has N, number of plays, incremented
    If node's parent is dark (1), then node's value increases
    Otherwise, node's value decreases.

    Args:
        node (Node): Leaf node from which rollout started.
        utility (int): Utility of simulated rollout.
    """
    while node is not None:
        node.N += 1
        if node.player == 1:
            node.value -= utility
        else:
            node.value += utility
        node = node.parent


def mcts(state, player, rollouts=100, alpha=5):
    # MCTS main loop: Execute four steps rollouts number of times
    # Then return successor with highest number of rollouts
    root = Node(state, player, None, [], 0, 1)
    for i in range(rollouts):
        leaf = select(root, alpha)
        new = expand(leaf)
        utility = simulate(new)
        backprop(new, utility)

    move = None
    plays = 0
    for m in get_possible_moves(state, player):
        s = play_move(state, player, m[0], m[1])
        if root.get_child(s).N > plays:
            plays = root.get_child(s).N
            move = m

    return move


####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("MCTS AI")        # First line is the name of this AI
    color = int(input())    # 1 for dark (first), 2 for light (second)

    while True:
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()

        if status == "FINAL":
            print()
        else:
            board = np.array(eval(input()))
            movei, movej = mcts(board, color)
            print("{} {}".format(movei, movej))


if __name__ == "__main__":
    run_ai()