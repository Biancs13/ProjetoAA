from ambientes.ambiente import Ambiente
from objetos.posicao import getDistancia

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

    def getRecompensa(self,pos,numColetaveis=0):
        #NOTA: AINDA NÂO INTRODUZ NOVELTY
        if pos == self.getPosicaoElementoMaisProximo(pos,'farol'):
            return 500
        ele = self.getElemento(pos)
        if ele.isSolido() or ele.getId() == (-1,0,-1):
            return -80
        return 0

