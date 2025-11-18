import random

class Agente:
    def __init__(self, id, posicaoAtual, sensor):
        self.id = id
        self.posicaoAtual = posicaoAtual
        self.sensor = sensor

    def getId(self):
        return self.id

    def getPosicao(self):
        return self.posicaoAtual

    # def cria(self,ficheiro):

    # observacao(self,obs)):

    # age(self):

    # avaliacaoEstadoAtual(self,recompensa):

    # instala(self,sensor):

    def getSensor(self):
        return self.sensor

    # ageAleatorio(self):







