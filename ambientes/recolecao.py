import time

from agentes.agente import estaFora
from ambientes.ambiente import Ambiente
from objetos.acao import mesma_direcao
from objetos.posicao import dentroLimites, getDistancia


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


    def getRecompensa(self,posAntiga,pos,angulo,numColetaveis=0,pts=0):
        #Falta novelty
        if not dentroLimites(pos,self.tamanhoGrelha):
            return -50
        ele = self.getElemento(pos)
        if ele.isSolido():
            return -80
        if ele.isColetavel():
            return ele.getPontos() * 150
        if ele.getNome() == "ninho":
            if pts == 0:
                return -25
            else:
                return pts * 150 + 300

        recompensa = 0
        ovo_pos = self.getPosicaoElementoMaisProximo(pos, "ovo")
        if ovo_pos != None:
            if getDistancia(posAntiga, ovo_pos) > getDistancia(pos, ovo_pos):
                recompensa += 40
            elif  getDistancia(posAntiga, ovo_pos) < getDistancia(pos, ovo_pos):
                recompensa -= 20


        ninho_pos = self.getPosicaoElementoMaisProximo(pos,"ninho")
        if getDistancia(posAntiga, ninho_pos) > getDistancia(pos, ninho_pos) and numColetaveis > 0:
            recompensa += 50

        recompensa -=1
        return  recompensa

