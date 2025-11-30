import time

from ambientes.ambiente import Ambiente


class Recolecao(Ambiente):
    def __init__(self, tamanho,tempoLimite):
        super().__init__(tamanho)
        self.tempoLimite = tempoLimite
        self.tempoInicial = time.time()
        self.totalPontosRecolhidos = 0


    def recolher(self,pontosTotais):
        self.totalPontosRecolhidos += pontosTotais


    def condicaoFim(self, agentes=None):
        return time.time() - self.tempoInicial >= self.tempoLimite