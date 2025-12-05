import time

from ambientes.ambiente import Ambiente


class Recolecao(Ambiente):
    def __init__(self, tamanho,tempoLimite):
        super().__init__(tamanho)
        self.tempoLimite = tempoLimite
        self.tempoInicial = time.time()
        self.pontos_totais = 0


    def adicionarPontos(self,pontos):
        self.pontos_totais += pontos

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


    def getRecompensa(self,pos,numColetaveis=0,pts=0):
        #Falta novelty
        ele = self.getElemento(pos)
        if ele.isSolido() or ele.getId() == (-1,0,-1):
            return -80
        if ele.isColetavel():
            return ele.getPontos() * 50
        if ele.getNome() == "ninho":
            if numColetaveis == 0:
                return -200
            else:
                return pts * 50 + 100
        return 0

