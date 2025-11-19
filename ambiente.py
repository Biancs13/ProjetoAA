from observacao import Observacao
from posicao import Posicao


class Ambiente:
    def __init__(self,gridSize):
        self.grelha = {Posicao(x,y):None for x in range(gridSize) for y in range(gridSize)}

    def observacaoParaAgente(self,agente):
        sensor = agente.getSensor()
        observacao = Observacao()
        for v in sensor.getCampoVisao():
            posicao = v.soma(agente.getPosicao())
            observacao.adicionar(v,self.grelha[posicao].getId())

    def agir(self,acao,agente):
        reward = 100
        return reward
