import random
from acao import *
from posicao import dentroLimites


class Agente:
    def __init__(self, id, posicaoAtual,angulo=0):
        self.id = id
        self.posicaoAtual = posicaoAtual
        self.sensor = None
        self.angulo = angulo

    def getId(self):
        return self.id

    def getPosicao(self):
        return self.posicaoAtual

    # def cria(self,ficheiro):

    # observacao(self,obs)):

    # age(self):

    # avaliacaoEstadoAtual(self,recompensa):

    def instala(self,sensor):
        self.sensor = sensor

    def getSensor(self):
        #Nota: tem de ser chamado depois de mudar a posição!
        return self.sensor

    def ageAleatorio(self,maxGrid):
        while True:
            acao = getAcaoAleatoria()
            novaPos, novoAng = atuar(self, acao)
            if novoAng != self.angulo:
                print("rodei")
                self.rodar(novoAng)
                break
            if dentroLimites(novaPos, maxGrid):
                self.posicaoAtual = novaPos
                break
            return novaPos,novoAng


    def rodar(self,novoAng):
        if self.sensor is not None:
            self.angulo = novoAng
            self.sensor.rodar()

    def __str__(self):
        return f"Agente {self.id}: Posicao={self.posicaoAtual}, Angulo={self.angulo}°"

agente = Agente(1,Posicao(0,0),0)
print(agente)
agente.ageAleatorio(20)
print(agente)

