import copy
import random
from enum import Enum
from posicao import *
from vetor import Vetor, vetor_para_angulo, normalizarVetor


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




def melhor_acao_para_direcao(anguloAgente, direcao):
    return melhor_acao(anguloAgente,vetor_para_angulo(direcao))


def melhor_acao(angA,angD):
    print(f"anguloA: {angA} | anguloD: {angD}")
    if angA == 0:
        if  angD < 45 or angD >= 315:
            return Acao.FRENTE
        elif 45 <= angD < 135:
            return Acao.DIREITA
        elif 135 <= angD < 225:
            return Acao.MEIA_VOLTA
        else:
            return Acao.ESQUERDA
    elif angA == 90:
        if angD < 45 or angD >= 315:
            return Acao.ESQUERDA
        elif 45 <= angD < 135:
            return Acao.FRENTE
        elif 135 <= angD < 225:
            return Acao.DIREITA
        else:
            return Acao.MEIA_VOLTA
    elif angA == 180:
        if angD < 45 or angD >= 315:
            return Acao.MEIA_VOLTA
        elif 45 <= angD < 135:
            return Acao.ESQUERDA
        elif 135 <= angD < 225:
            return Acao.FRENTE
        else:
            return Acao.DIREITA
    else:
        if angD < 45 or angD >= 315:
            return Acao.DIREITA
        elif 45 <= angD < 135:
            return Acao.MEIA_VOLTA
        elif 135 <= angD < 225:
            return Acao.ESQUERDA
        else:
            return Acao.FRENTE


def angulo_desvio(vetor_objetivo, acao, angulo_agente):
    acoes_locais = {
        Acao.FRENTE: (1, 0),
        Acao.ESQUERDA: (0, 1),
        Acao.DIREITA: (0, -1),
        Acao.MEIA_VOLTA: (-1, 0)
    }
    x, y = acoes_locais[acao]

    rad = math.radians(angulo_agente)
    x_rot = x * math.cos(rad) - y * math.sin(rad)
    y_rot = x * math.sin(rad) + y * math.cos(rad)

    fx, fy = vetor_objetivo.x, vetor_objetivo.y
    dot = x_rot * fx + y_rot * fy
    mag_a = math.sqrt(x_rot ** 2 + y_rot ** 2)
    mag_f = math.sqrt(fx ** 2 + fy ** 2)

    if mag_a == 0 or mag_f == 0:
        return math.pi
    cos_theta = max(min(dot / (mag_a * mag_f), 1), -1)
    return math.acos(cos_theta)



