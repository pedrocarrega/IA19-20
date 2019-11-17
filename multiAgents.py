# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

from pacman import Directions


import game



from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

from collections import namedtuple
import random

from utils import argmax

infinity = float('inf')
ClassicPac = namedtuple('ClassicPac', 'to_move, board, extra',defaults=[None])

class ClassicPacman:
    """A game is similar to a problem, but it has a utility for each
    state and a terminal test instead of a path cost and a goal
    test. To create a game, subclass this class and implement actions,
    result, utility, and terminal_test. You may override display and
    successors or you can inherit their default methods. You will also
    need to set the .initial attribute to the initial state; this can
    be done in the constructor.
    """
    
    def __init__(self,initial):
        self.initial = initial

    def actions(self, state):
        """Return a list of the allowable moves at this point.
        by default, actions for Pacman, agent index 0.
        ghosts start at 1
        """
        if state.to_move == "Pacman":
            return state.board.getLegalActions()
        else:
            return state.board.getLegalActions(1)

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        if state.to_move == "Pacman":
            return ClassicPac(board=state.board.generatePacmanSuccessor(move),to_move="Ghosts")
        else:
            return ClassicPac(board=state.board.generateSuccessor(1,move),to_move="Pacman")

    def utility(self, state, player):
        """Return the value of this final state to player which will be the score."""
        if player == "Pacman":
            return state.board.get_score()
        else:
            return -state.board.get_score()

    def terminal_test(self, state):
        """Return True if this is a final state for the game.
        No actions mean a terminal state
        """
        return not self.actions(state)

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move

    def display(self, state):
        """Print or otherwise display the state."""
        print("Next move:",state.to_move)
        print(state.board)


def alphabeta_cutoff_search(state, game, d=4, cutoff_test=None, eval_fn=None):
    """Search game to determine best action; use alpha-beta pruning.
    This version cuts off search and uses an evaluation function."""

    player = game.to_move(state)

    # Functions used by alphabeta
    def max_value(state, alpha, beta, depth):
        #print(depth)
        if cutoff_test(state, depth):
            return eval_fn(state,player)
        v = -infinity
        for a in game.actions(state):              ##
            v = max(v, min_value(game.result(state, a),
                                 alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        #print(depth)
        if cutoff_test(state, depth):
            return eval_fn(state,player)
        v = infinity
        for a in game.actions(state):              ##
            v = min(v, max_value(game.result(state, a),
                                 alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_cutoff_search starts here:
    # The default test cuts off at depth d or at a terminal state
    cutoff_test = (cutoff_test or
                   (lambda state, depth: depth > d or
                    game.terminal_test(state)))
    eval_fn = eval_fn or (lambda state: game.utility(state, player))
    best_score = -infinity
    beta = infinity
    best_action = None
    movimentos = game.actions(state)  ## jb
    random.shuffle(movimentos)        ## para dar variabilidade aos jogos
    for a in movimentos:              ##
        v = min_value(game.result(state, a), best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = a
    return best_action




def manhatanDist(p1,p2):
        p1x,p1y=p1
        p2x,p2y=p2
        return abs(p1x-p2x)+abs(p1y-p2y)

def so_score(gState,player):
    return gState.board.getScore()
    
    
def anti_score(gState,player):
    return -gState.board.getScore()
    
def scooore(gState,player):
    foodList = gState.board.getFood().asList()
    minDistance = 0
    # Compute distance to the nearest food
    if len(foodList) > 0: # This should always be True,  but better safe than sorry
        myPos = gState.board.getPacmanPosition()
        
        minDistance = min([manhatanDist(myPos, food) for food in foodList])
    return gState.board.getScore() * 100 - minDistance






class MultiAgentSearchAgent(Agent):
    """
     This class provides the constructor with additional two attributes: depth and evaluationFunction, and a default name to 
    every subclass
    """

   # def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    def __init__(self, index=0,evalFn = 'so_score', depth = '2'):
        self.index = index  #0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
        
    def myName(self):
        #return self.__class__.__name__ + self.evaluationFunction.__name__
        return self.evaluationFunction.__name__

    
    
class AlphaBetaGhost(MultiAgentSearchAgent):
    """
    Your minimax ghost with alpha-beta pruning 
    """


    def getAction(self, gameState):
        """
        Returns the alfabeta action using self.depth and self.evaluationFunction
        """
        
        
        currentState = ClassicPac(to_move="Ghost",board=gameState)
        thisGame = ClassicPacman(currentState)
        #print("UAU. here goes alpha beta")
        return alphabeta_cutoff_search(currentState, thisGame, d=self.depth, eval_fn=anti_score)




class AlphaBetaAgent(MultiAgentSearchAgent):
    """
     The alpha-beta pruning Pacman (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """

        currentState = ClassicPac(to_move="Pacman",board=gameState)
        thisGame = ClassicPacman(currentState)
        #print("UAU. here goes alpha beta")
        return alphabeta_cutoff_search(currentState, thisGame, d=self.depth, eval_fn=self.evaluationFunction)
        
        
# ----------------  Random Agents

class RandomPac(Agent):
    """ A pacman that chooses its actions in a random way"""
    
    def getAction(self, state):
        # Generate candidate actions
        legal = state.getLegalPacmanActions()
        return random.choice(legal)
    
class RandomGhost(Agent):
    """ A ghost that chooses its actions in a random way"""
    
    def getAction(self, state):
        # Generate candidate actions
        legal = state.getLegalActions(self.index)
        return random.choice(legal)




