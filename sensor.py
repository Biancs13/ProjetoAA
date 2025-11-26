import math

from acao import getVetorFrente
from vetor import Vetor, multiplicar_vetor_matriz


#Para manter o sensor sempre ordenado em esquerda frente direita (independentemente do angulo)
def anguloEntre(vetor,frente):
    cruzado = vetor.x * frente.y - vetor.y * frente.x
    escalar = vetor.x * frente.x + vetor.y * frente.y
    return math.atan2(cruzado, escalar)


class Sensor:
    def __init__(self, campoVisao,anguloInicial = 0):
        self.campoVisao = campoVisao
        self.ordenar(anguloInicial)

    def getCampoVisao(self):
        return self.campoVisao

#fazer função para rodar os digs
    def rodar(self, rotacao,NovoAngulo):
        novoCampoVisao = []
        for v in self.campoVisao:
            novoCampoVisao.append(rodar(v, rotacao))
        self.campoVisao = novoCampoVisao
        self.ordenar(NovoAngulo)

    def ordenar(self,angulo):
        self.campoVisao.sort(key=lambda v: anguloEntre(v, getVetorFrente(angulo)))


def rodar(vetor,angulo):
    if angulo == 0:
        return vetor
    elif angulo == 90:
        matriz = [[0, -1], [1, 0]]
    elif angulo == 180:
        matriz = [[-1, 0], [0, -1]]
    else:
        matriz = [[0, 1], [-1, 0]]
    res = multiplicar_vetor_matriz(vetor,matriz)
    return res

