from abc import ABC

from agente import Agente


class AgenteFixo(Agente):

    def __init__(self, id, posicaoInicial, angulo):
        super().__init__(id,posicaoInicial,angulo)
        self.posiccoesBloqueadas = []
        self.ultimaPosicao = posicaoInicial

    def age(self):
        pass

    def avaliacaoEstadoAtual(self,recompensa):
        pass


