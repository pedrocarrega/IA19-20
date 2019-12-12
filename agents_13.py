from pacman import Directions

import game

from multiAgents import *

from distanceCalculator import *

#from util import manhatanDist
from game import Directions
import random, util

from game import Agent

from collections import namedtuple
import random

from utils import argmax

def extraP_13(gState,extra):
    if extra == {}:
        distancer = Distancer(gState.data.layout)
        distancer.getMazeDistances()
        n_extra ={'Moves':[gState.getPacmanPosition()],'Distance':distancer}
        return n_extra
    else:
        n_extra=extra.copy()
        if (len(n_extra['Moves']) == 5):
            n_extra['Moves'] = n_extra['Moves'][1:] + [gState.getPacmanPosition()]
        else:
            n_extra['Moves'] = n_extra['Moves'] + [gState.getPacmanPosition()]
    return n_extra
    

def extraF_13(gState,extra):
    """ memorizes the positions of ghosts
    """
    if extra == {}:
        n_extra ={'Ghosts':[gState.getGhostPosition(1)]} #,'ini':[gState.getGhostPosition(1)]} crasha isto
        return n_extra
    else:
        n_extra=extra.copy()
        n_extra['Ghosts']=[gState.getGhostPosition(1)]+n_extra['Ghosts']
    return n_extra

def pac_13(gState, player):
    scared = 0
    repeat = 0
    
    #if gState.board.getPacmanPosition() in gState.extra['Moves']:
    #    repeat = -100

    #print(gState.extra['Distance'].getDistance(gState.board.getPacmanPosition(), gState.board.getGhostState(1).getPosition()))

    if (gState.board.getGhostState(1).scaredTimer > 7) & (manhatanDist_13(gState.board.getPacmanPosition(), gState.board.getGhostState(1).getPosition()) > 15):
        scared += manhatanDist_13(gState.board.getPacmanPosition(), gState.board.getGhostState(1).getPosition()) * 100
    foodList = gState.board.getFood().asList()
    minDistance = 0
    # Compute distance to the nearest food
    if len(foodList) > 0: # This should always be True,  but better safe than sorry
        myPos = gState.board.getPacmanPosition()
        
        minDistance = min([manhatanDist_13(myPos, food) for food in foodList])
    return gState.board.getScore() * 100 - minDistance + scared + repeat




def fant_13(gState, player):
    
    lose = 0
    run = 0
    position = 0
    capsuleList = gState.board.getCapsules()
    dist = 0
     
    """ forcar o gajo a nao ir para uma posicao onde ja esteve"""
    #if (manhatanDist_13(gState.board.getGhostPosition(1),gState.extra['ini'][0]) <6 ): crasha isto tudo
    leg = gState.board.getLegalActions(1)
    for x in leg:
        g1 = gState.board.generateSuccessor(1,x)
        for y in gState.extra['Ghosts']: #do extra_mem
            if (g1.getGhostPosition(1) == y):
                #print(y)
                dist = -10000
    
    """apenas uma experiencia, tenta obrigar o fantasma a ir atras do pacman, parece funcional -> ver replay.
        problema-> o fantasma so comeca a fugir quando ja eh tarde demais, eh quase sempre apanhado ->alias penso que nao estah a fugir sequer
        (corrido apenas com os ifs do lose e do run,tudo o resto comentado, e return -(gState.board.getScore()) - p + run """ 
    leg = gState.board.getLegalActions(1)
    k= 0
    p= 0
    for x in leg:
        g1 = gState.board.generateSuccessor(1,x)
        k = manhatanDist_13(gState.board.getPacmanPosition(),g1.getGhostPosition(1))
        #print (k)
        if p == 0:
            p = k
        else:
            if p>k:
                p = k
                #print("vai mudar")
                #print(p)
                
    if(gState.board.isLose()):
        lose = -10000
    
    if(direction_13(gState.board.getPacmanPosition(), gState.board.getGhostState(1).getPosition()) == gState.board.getGhostState(1).getDirection()):
        #print(direction_13(gState.board.getPacmanPosition(), gState.board.getGhostState(1).getPosition()))
        position = -500
    
    # Compute distance to the nearest food
    if len(capsuleList) > 0: # This should always be True,  but better safe than sorry
        if (min([manhatanDist_13(gState.board.getPacmanPosition(), capsule) for capsule in capsuleList])) > 5 & (manhatanDist_13(gState.board.getPacmanPosition(), gState.board.getGhostState(1).getPosition()) > 5):
            run += 1000

    #return -(gState.board.getScore()) + run
    return lose + run + position + dist




def manhatanDist_13(p1,p2):
        p1x,p1y=p1
        p2x,p2y=p2
        return abs(p1x-p2x)+abs(p1y-p2y)

def direction_13(p1,p2):
    p1x,p1y=p1
    p2x,p2y=p2
    x = p1x - p2x
    y = p1y - p2y
    if(abs(x) > abs(y)):
        if x > 0:
            return 'North'
        if x < 0:
            return 'South'
    else:
        if y > 0:
            return 'East'
        if y < 0:
            return 'West'
