def pac_13(gState, player):
    
    scared = 0
    repeat = 0
    minDistance = 0
    
    if (gState.board.getGhostState(1).scaredTimer > 7) & (manhatanDist_13(gState.board.getPacmanPosition(), gState.board.getGhostState(1).getPosition()) > 15):
        scared += manhatanDist_13(gState.board.getPacmanPosition(), gState.board.getGhostState(1).getPosition()) * 100
        
    foodList = gState.board.getFood().asList()
    
    if len(foodList) > 0:
        myPos = gState.board.getPacmanPosition()
        
        minDistance = min([manhatanDist_13(myPos, food) for food in foodList])
    return gState.board.getScore() * 100 - minDistance + scared


def fant_13(gState, player):
    
    """run fantasma run - fantasma procura afastar -se o maximo do pacman"""
    leg = gState.board.getLegalActions(1) #para saber as accoes possiveis do fantasma no instante atual
    k = 0
    p = 0
    
    for x in leg: #para cada accao possivel,
        g1 = gState.board.generateSuccessor(1,x) #gerar um estado sucessor dessa accao
        k = manhatanDist_13(gState.board.getPacmanPosition(),g1.getGhostPosition(1)) #ver a que distancia fica o fantasma do pacman nesse estado sucessor 
        
        if p == 0: #se eh a primeira accao do ciclo, manter esse valor em p
            p = k 
        else:
            if p<k: #caso seja encontrado um estado sucessor cuja distancia ao pacman eh maior que o valor atual em p, atualizar p
                p = k
    return p 


def manhatanDist_13(p1,p2):
        p1x,p1y=p1
        p2x,p2y=p2
        return abs(p1x-p2x)+abs(p1y-p2y)