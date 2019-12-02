from pacman import Directions


import game



from multiAgents import manhattanDistance
from game import Directions
import random, util

from game import Agent

from collections import namedtuple
import random
import multiAgents

from utils import argmax

def pac_13(gState, player):
    foodList = gState.board.getFood().asList()
    minDistance = 0
    # Compute distance to the nearest food
    if len(foodList) > 0: # This should always be True,  but better safe than sorry
        myPos = gState.board.getPacmanPosition()
        
        minDistance = min([manhatanDist(myPos, food) for food in foodList])
    return gState.board.getScore() * 100 - minDistance




#def fant_13(gState, player):

