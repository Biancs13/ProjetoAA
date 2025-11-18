from enum import Enum
from posicao import Posicao

def Acao(Enum):
    DIREITA = (1,0)
    ESQUERDA = (-1,0)
    CIMA =  (0,-1)
    BAIXO =  (0,1)

    def getNovaPosicao(p):
        x = p.getX()
        y = p.getY()
        if p == DIREITA:
            return Posicao(x+1,y)
        elif p == ESQUERDA:
            return Posicao(x-1,y)
        elif p == CIMA:
            return Posicao(x,y-1)
        return Posicao(x,y+1)

