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
        found_grelha = False
        found_agente = False
        for p,ele in self.grelha.items():
            if ele.isColetavel():
                found_grelha = True
                break
        if not found_grelha:
            for a in agentes:
                if len(a.getColetaveis()) > 0:
                    found_agente= True
                    break
        return (not found_grelha and not found_agente) or time.time() - self.tempoInicial >= self.tempoLimite