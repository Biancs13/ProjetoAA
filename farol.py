from ambiente import Ambiente
from posicao import getDistancia

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

