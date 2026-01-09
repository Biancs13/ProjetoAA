from ambientes.ambiente import Ambiente
from objetos.posicao import getDistancia, dentroLimites


class Labirinto(Ambiente):
    def __init__(self,tamanho):
        super().__init__(tamanho)

    def getDistanciaSaida(self,agente):
        saidas = self.getElementos('saida')
        if not saidas:
            return None
        for pos in saidas:
            return getDistancia(pos, agente.getPosicao())

    def condicaoFim(self, agentes):
        for agente in agentes:
            dist = self.getDistanciaSaida(agente)
            if dist == 0:
                return True
        return False

    def getRecompensa(self,posAntiga,pos,angulo,num_coletaveis=0,pts=0):

        if not dentroLimites(pos, self.tamanhoGrelha):
            return -0.5
        '''
        if self.getElemento(pos).isSolido():
            return -0.5
        '''
        saida = self.getPosicaoElementoMaisProximo(pos, "saida")
        if pos == saida:
            return 100
        return -0.1


    def calcular_fitness(self,agente):
        recompensa = agente.num_colisoes * -0.5
        recompensa -= len(agente.comportamento) * 0.1
        saida_pos = self.getPosicaoElementoMaisProximo(agente.posicaoAtual, "saida")
        if getDistancia(saida_pos, agente.posicaoAtual) == 0:
            recompensa += 100
        else:
            recompensa += 90 // getDistancia(saida_pos, agente.posicaoAtual)
        return recompensa