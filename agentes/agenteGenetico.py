from abc import ABC

from agentes.agente import Agente



class AgenteGenetico(Agente):

    def __init__(self, id, posicaoInicial, tipo, angulo):
        super().__init__(id,posicaoInicial,tipo, angulo)
        self.posiccoesBloqueadas = []
        self.ultimaPosicao = posicaoInicial

    def age(self):
        pass

    def avaliacaoEstadoAtual(self,recompensa):
        pass