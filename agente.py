import random
from acao import *
from posicao import dentroLimites


class Agente:
    def __init__(self, id, posicaoAtual,angulo=0):
        self.id = id
        self.posicaoAtual = posicaoAtual
        self.sensor = None
        self.angulo = angulo
        self.coletaveis = []
        self.observavaoAtual = None

    def getId(self):
        return self.id

    def getPosicao(self):
        return self.posicaoAtual

    def observacao(self,obs):
        self.observavaoAtual = obs

    #Não Altera o agente
    def age(self):
        pass

    def avaliacaoEstadoAtual(self,recompensa):
        pass

    def instala(self,sensor):
        if self.sensor is None:
            self.sensor = sensor
        else:
            self.sensor.getCampoVisao().append(sensor.getCampoVisao())

    def getSensor(self):
        return self.sensor

    #Não Altera o agente
    def ageAleatorio(self,maxGrid):
        while True:
            acao = getAcaoAleatoria()
            novaPos, novoAng = atuar(self, acao)

            if novoAng != self.angulo:
                return novaPos, novoAng
            if dentroLimites(novaPos, maxGrid):
                return novaPos, novoAng
            #return novaPos,novoAng


    def rodar(self,novoAng):
        if self.sensor is not None:
            self.angulo = novoAng
            self.sensor.rodar()

    def coleta(self,elemento):
        if elemento.isColetavel():
            self.coletaveis.append(elemento)


    def alterar(self,novaPos,novoAng):
        self.rodar(novoAng)
        self.posicaoAtual = novaPos

    def __str__(self):
        return f"Agente {self.id}: Posicao={self.posicaoAtual}, Angulo={self.angulo}°"

#Lara
def cria(linha):
    pass
