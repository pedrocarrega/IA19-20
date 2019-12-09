from pacman import Directions

import game

from multiAgents import *

#from util import manhatanDist
from game import Directions
import random, util

from game import Agent

from collections import namedtuple
import random

from utils import argmax

def extraP_13(gState,extra):
    """ vai memorizar onde se encontra o fantasma e as super pastilhas, pq no scooore por vezes
        o efeito das superpastlhas n eh aproveitado -> arranjar maneira do gajo so apanhar a pastilha
        quando realmente de para comer o fantasma -> mas optando no entanto por nao comer o fantasma
        caso esteja a x casas da posicao onde o fantasma respawns (acho que no scooore isto ja acontece)
    """
    if extra == {}:
        n_extra ={'super':[gState.getCapsules()],'Ghosts':[gState.getGhostPosition(1)],}
        return n_extra
    else:
        n_extra=extra.copy()
        n_extra['super'] =[gState.getCapsules()] + n_extra['super'] #?
        n_extra['Ghosts']=[gState.getGhostPosition(1)]+n_extra['Ghosts']
    return n_extra
#outra cena a alterar se possivel seria diminuir as vezes que o pacman fica indeciso,  -> ver recordedgamepac_404 
#alguma ideia porque isto acontece?

def pac_13(gState, player):
    scared = 0
    if (gState.board.getGhostState(1).scaredTimer > 7) & (manhatanDist_13(gState.board.getPacmanPosition(), gState.board.getGhostState(1).getPosition()) > 15):
        scared += 100000
        if gState.board.getPacmanState().getDirection() == gState.board.getGhostState(1).getDirection(): #need to check this if
            scared -= 500
    foodList = gState.board.getFood().asList()
    minDistance = 0
    # Compute distance to the nearest food
    if len(foodList) > 0: # This should always be True,  but better safe than sorry
        myPos = gState.board.getPacmanPosition()
        
        minDistance = min([manhatanDist_13(myPos, food) for food in foodList])
    return gState.board.getScore() * 100 - minDistance + scared




def fant_13(gState, player):
    
    lose = 0
    run = 0
    position = 0
    capsuleList = gState.board.getCapsules()
    
    if(gState.board.isLose()):
        lose = -10000
    
    if(direction_13(gState.board.getPacmanPosition(), gState.board.getGhostState(1).getPosition()) == gState.board.getGhostState(1).getDirection()):
        position = -500
    
    # Compute distance to the nearest food
    if len(capsuleList) > 0: # This should always be True,  but better safe than sorry
        if (min([manhatanDist_13(gState.board.getPacmanPosition(), capsule) for capsule in capsuleList])) > 5 & (manhatanDist_13(gState.board.getPacmanPosition(), gState.board.getGhostState(1).getPosition()) > 5):
            run -= 1000

    #return -(gState.board.getScore()) + run
    return -(gState.board.getScore()) + lose + run + position




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
