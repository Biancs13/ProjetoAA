import random
from abc import ABC

from agentes.agente import Agente
from objetos.acao import getAcaoAleatoria, Acao


class AgenteReforco(Agente):

    def __init__(self, id, posicaoInicial, tipo, angulo,tx_aprendizagem,desconto,exploracao):
        super().__init__(id,posicaoInicial,tipo, angulo)
        self.q = {} # Dicionario de dicionarios, para cada estado damos um dicionario com acao,Q
        self.tx_aprendizagem = tx_aprendizagem
        self.desconto = desconto
        self.exploracao = exploracao
        self.ultima_acao = None

    def age(self):
        self.ultima_acao = self.escolher_acao(self.estadoAntigo)
        return self.ultima_acao

    def escolher_acao(self,s):
        if random.random() < self.exploracao:
            return getAcaoAleatoria()
        else:
            return self.getAcaoComMaiorQ(s)

    def getAcaoComMaiorQ(self,estadoAtual):
        if estadoAtual not in self.q:
            self.q[self.estadoAntigo] = {acao: 0 for acao in list(Acao)}
            return getAcaoAleatoria()

        dic_acoes = self.q[estadoAtual]
        max_q = max(dic_acoes.values())
        melhores_acoes = [acao for acao, q in dic_acoes.items() if q == max_q]
        return random.choice(melhores_acoes) # para lidar com empates


    #na verdade aqui é avaliacao do EstadoAntigo  Podemos mudar

    def avaliacaoEstadoAtual(self,recompensa):

        if self.estadoAntigo not in self.q:
            self.q[self.estadoAntigo] = {acao: 0 for acao in list(Acao)}

        q_atual = self.q[self.estadoAntigo][self.ultima_acao]

        if self.estadoAtual not in self.q:
            self.q[self.estadoAtual] = {acao: 0 for acao in list(Acao)}

        max_q_novo = max(self.q[self.estadoAtual].values(), default=0)

        self.q[self.estadoAntigo][self.ultima_acao] =(
                q_atual + self.tx_aprendizagem * (recompensa + self.desconto*max_q_novo - q_atual))



