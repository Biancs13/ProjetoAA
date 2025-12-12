from ambientes.ambiente import Ambiente
from objetos.acao import mesma_direcao
from objetos.posicao import getDistancia, dentroLimites


class Farol(Ambiente):
    def __init__(self,tamanho):
        super().__init__(tamanho)

    def getDistanciaFarol(self, agente):
        farois = self.getElementos('farol')
        if not farois:
            return None
        for pos in farois:
            return getDistancia(pos, agente.getPosicao())

    def condicaoFim(self,agentes):
        for agente in agentes:
            dist = self.getDistanciaFarol(agente)
            if dist == 0:
                return True
        return False

    def getRecompensa(self,posAntiga,pos,angulo,num_coletaveis=0,pts=0):
        if not dentroLimites(pos, self.tamanhoGrelha):
            return -50
        if self.getElemento(pos).isSolido():
            return -50
        farol = self.getPosicaoElementoMaisProximo(pos, "farol")
        if pos == farol:
            return 500
        return -1

