from ambientes.ambiente import Ambiente
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

    def getRecompensa(self,pos,numColetaveis=0,pts=0):
        #NOTA: AINDA NÂO INTRODUZ NOVELTY
        if not dentroLimites(pos,self.tamanhoGrelha):
            return -40
        if pos == self.getPosicaoElementoMaisProximo(pos,'farol'):
            return 500
        ele = self.getElemento(pos)
        if ele.isSolido():
            return -40
        return -0.3

