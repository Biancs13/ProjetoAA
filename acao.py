from enum import Enum
from posicao import Posicao

def Acao(Enum):
    DIREITA = (1,0,0)
    ESQUERDA = (-1,0,0)
    CIMA =  (0,-1,0)
    BAIXO =  (0,1,0)
    RODAR = (0,0,90)

    def getNovaPosicao(p):
        x = p.getX()
        y = p.getY()
        a = p.getAngulo()
        if p == DIREITA:
            return Posicao(x+1,y,a)
        elif p == ESQUERDA:
            return Posicao(x-1,y,a)
        elif p == CIMA:
            return Posicao(x,y-1,a)
        elif p == BAIXO:
            return Posicao(x,y+1,a)
        return Posicao(x,y,(a + 90) % 360)

