#!/usr/bin/env python3
# -*- coding: utf-8 -*
"""
Alpha-beta minimax AI player for Othello.
"""

import numpy as np
from six.moves import input
from othello_shared import get_possible_moves, play_move, compute_utility


def max_value(state, player, alpha, beta):
    """
    Args:
        state: Board state
        player: Dark (1) or light (2)
        alpha, beta values

    Returns:
        value (int): Minimax value of state
        move (tuple): Best move to make
    """
    
    moves = get_possible_moves(state, player)
    if not moves:
        return compute_utility(state), None

    optimal_val = -float("inf")
    optimal_move = None
    for n in moves:
        next_state = play_move(state,player,n[0],n[1])
        if player == 2:
            next_player =1
        else:
            next_player = 2
        value, _ = min_value(next_state,next_player,alpha,beta)
        if value > optimal_val:
            optimal_val = value
            optimal_move = n
        if optimal_val >= beta:
            return optimal_val, optimal_move
        alpha = max(alpha, optimal_val)
    
    return optimal_val, optimal_move


def min_value(state, player, alpha, beta):
    """
    Args:
        state: Board state
        player: Dark (1) or light (2)
        alpha, beta values

    Returns:
        value (int): Minimax value of state
        move (tuple): Best move to make
    """
    moves = get_possible_moves(state, player)
    if not moves:
        return compute_utility(state), None

    optimal_val = float("inf")
    optimal_move = None
    for n in moves:
        next_state = play_move(state,player,n[0],n[1])
        if player == 2:
            next_player =1
        else:
            next_player = 2
        value, _ = max_value(next_state,next_player,alpha,beta)
        if value<optimal_val:
            optimal_val = value
            optimal_move = n
        if optimal_val <= alpha:
            return optimal_val, optimal_move
        beta = min(beta, optimal_val)
    return optimal_val, optimal_move


def minimax(state, player):
    """
    Minimax main loop
    Call max_value if player is 1 (dark), min_value if player is 2 (light)
    Then return the resultant move
    """
    if player == 1:
        _, move = max_value(state, player, -float('inf'), float('inf'))
    else:
        _, move = min_value(state, player, -float('inf'), float('inf'))
    return move


####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Minimax AI")     # First line is the name of this AI
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
            movei, movej = minimax(board, color)
            print("{} {}".format(movei, movej))


if __name__ == "__main__":
    run_ai()