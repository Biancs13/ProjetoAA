import copy
import random
from enum import Enum
from posicao import Posicao

class Acao(Enum):
    DIREITA = (1,0)
    ESQUERDA = (-1,0)
    CIMA =  (0,-1)
    BAIXO =  (0,1)
    RODAR = (0,0)

    def getNovaPosicao(self, posicao, angulo):
        if self == Acao.RODAR:
            return Posicao(posicao.x, posicao.y), (angulo + 90) % 360
        dx, dy = self.value
        return Posicao(posicao.x + dx, posicao.y + dy), angulo

def atuar(agente, acao):
    novaPos, novoAng = acao.getNovaPosicao(agente.posicaoAtual, agente.angulo)
    return novaPos, novoAng

def getAcaoAleatoria():
    return random.choice(list(Acao))

