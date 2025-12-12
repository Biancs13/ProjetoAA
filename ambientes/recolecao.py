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
            return -50
        if ele.isColetavel():
            return ele.getPontos() * 150
        if ele.getNome() == "ninho":
            if pts == 0:
                return -25
            else:
                return pts * 150 + 300


    def calcular_fitness(self,agente):
        recompensa = agente.num_colisoes * -20
        recompensa -= len(agente.comportamento) * 0.1
        recompensa += agente.num_coletaveis() * 80
        recompensa += agente.pontos() * 120
        ninho_pos = self.getPosicaoElementoMaisProximo(agente.posicaoAtual, "ninho")
        ovo_pos = self.getPosicaoElementoMaisProximo(agente.posicaoAtual, "ovo")
        if getDistancia(ninho_pos, agente.posicaoAtual) == 0:
            recompensa += 40
        else:
            recompensa += 30 // getDistancia(ninho_pos, agente.posicaoAtual)
        if ovo_pos is not None:
            if getDistancia(ovo_pos, agente.posicaoAtual) == 0:
                recompensa += 60
            else:
                recompensa += 50 // getDistancia(ovo_pos, agente.posicaoAtual)
        return recompensa

