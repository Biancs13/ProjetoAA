import copy
import random
from enum import Enum
from posicao import Posicao
from vetor import Vetor


class Acao(Enum):
    DIREITA = "D"
    ESQUERDA = "E"
    FRENTE = "F"
    MEIA_VOLTA = "M"

    def getNovaPosicao(self, posicao, angulo):
        if self == Acao.FRENTE:
            frente = getVetorFrente(angulo)
            novaPos = frente.soma(posicao)
            return novaPos, angulo
        elif self == Acao.MEIA_VOLTA:
            return posicao, normalizarAngulo(angulo + 180)
        elif self == Acao.ESQUERDA:
            novoAngulo = normalizarAngulo(angulo+270)
            frente = getVetorFrente(novoAngulo)
            novaPos = frente.soma(posicao)
            return novaPos, novoAngulo
        elif self == Acao.DIREITA:
            novoAngulo = normalizarAngulo(angulo+90)
            frente = getVetorFrente(novoAngulo)
            novaPos = frente.soma(posicao)
            return novaPos, novoAngulo


def normalizarAngulo(angulo):
    return angulo % 360

def atuar(agente, acao):
    novaPos, novoAng = acao.getNovaPosicao(agente.posicaoAtual, agente.angulo)
    return novaPos, novoAng

def getAcaoAleatoria():
    return random.choice(list(Acao))

def getVetorFrente(angulo):
    if angulo == 0:
        return Vetor(1,0)
    elif angulo == 90:
        return Vetor(0,1)
    elif angulo == 180:
        return Vetor(-1,0)
    elif angulo == 270:
        return Vetor(0,-1)
    else:
        raise ValueError(f"Angulo inválido: {angulo}")