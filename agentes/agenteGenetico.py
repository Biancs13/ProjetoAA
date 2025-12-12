import random
from agentes.agente import Agente, escrever
from ambientes.farol import Farol
from ambientes.recolecao import Recolecao
from objetos.acao import Acao, atuar
from objetos.posicao import getDistancia
from objetos.redeNeuronal import criarRedeNeuronal


class AgenteGenetico(Agente):

    def __init__(self, id, posicaoInicial, tipo, angulo, ficheiro):
        super().__init__(id,posicaoInicial,tipo, angulo,ficheiro)
        self.fitness = 0.0
        self.pesos = []
        self.rede_neuronal = None
        self.comportamento = []
        self.pontos_novelty=0.0

    def age(self):
        if self.rede_neuronal is None:
            self.rede_neuronal = criarRedeNeuronal(len(self.estadoAtual))
            self.rede_neuronal.carregaPesos(self.pesos)
        acao = self.rede_neuronal.decidirAcao(self.estadoAtual)
        self.comportamento.append(acao)
        self.num_passos += 1
        return acao

    def avaliacaoEstadoAtual(self,recompensa):
        self.fitness += recompensa

    def calcular_fitness_objetivo(self):
        total_pontos = self.fitness
        total_pontos += self.num_colisoes * -25
        total_pontos += len(self.comportamento) * -0.1
        if self.tipoProblema == "F":
            if self.condicaoFim:
                total_pontos+=500
        elif self.tipoProblema == "R":
            total_pontos += self.num_pontos_recolhidos * 100
        return total_pontos

    def escreverMelhor(self):
        escrever(self.ficheiro,self.pesos)

