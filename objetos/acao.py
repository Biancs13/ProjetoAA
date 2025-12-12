import copy
import random
from enum import Enum
from objetos.posicao import *
from objetos.vetor import *


class Acao(Enum):
    DIREITA = 0
    ESQUERDA = 1
    FRENTE = 2
    MEIA_VOLTA = 3

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

def atuar(posicao,angulo, acao):
    novaPos, novoAng = acao.getNovaPosicao(posicao, angulo)
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

def melhor_acao_para_direcao(anguloAgente, direcao):
    return melhor_acao(anguloAgente,vetor_para_angulo(direcao))

def mesma_direcao(angA,direcao):
    angulo = vetor_para_angulo(direcao)
    if angA -45 < angulo < angA + 45:
        return True
    else:
        return False

# o angulo dado é dependente do agente
def melhor_acao(ang):
    if 0 <= ang < 45:
        return Acao.DIREITA
    elif 45 <= ang < 135:
        return Acao.FRENTE
    elif 135 <= ang < 180:
        return Acao.ESQUERDA
    else:
        return Acao.MEIA_VOLTA