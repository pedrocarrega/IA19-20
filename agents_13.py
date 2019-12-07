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
    foodList = gState.board.getFood().asList()
    minDistance = 0
    # Compute distance to the nearest food
    if len(foodList) > 0: # This should always be True,  but better safe than sorry
        myPos = gState.board.getPacmanPosition()
        
        minDistance = min([manhatanDist(myPos, food) for food in foodList])
    return gState.board.getScore() * 100 - minDistance




#def fant_13(gState, player):

