import time

from ambiente import Ambiente


class Recolecao(Ambiente):
    def __init__(self, tamanho,tempoLimite):
        super().__init__(tamanho)
        self.tempoLimite = tempoLimite
        self.tempoInicial = time.time()

    def getNinhoMaisProximo(self, agente):
        ninhos = self.getElementos('ninho')
        if not ninhos:
            return None
        agente_pos = agente.getPosicao()
        ninho_mais_proximo = min(ninhos.items(), key=lambda item: item[0].getDistancia(agente_pos))
        return ninho_mais_proximo


    def condicaoFim(self, agentes=None):
        return time.time() - self.tempoInicial >= self.tempoLimite