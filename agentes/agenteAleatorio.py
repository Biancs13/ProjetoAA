from objetos.acao import Acao,getAcaoAleatoria
from agentes.agente import Agente, escrever


class AgenteAleatorio(Agente):

    def __init__(self, id, posicaoInicial, tipo, angulo,ficheiro):
        super().__init__(id,posicaoInicial,tipo, angulo,ficheiro)
        self.acoes = []

    def age(self):
        print(self.estadoAtual)
        elementos = self.estadoAtual[1:10]
        while True:
            acao = getAcaoAleatoria()

            if estaFora(elementos,acao):
                continue

            if existeSolido(elementos,acao):
                continue

            self.acoes.append(acao)
            return acao


    def avaliacaoEstadoAtual(self,recompensa):
        pass

    def escreverMelhor(self):
        escrever(self.ficheiro,self.acoes)


def existeSolido(elementos,acao):
    if acao == Acao.ESQUERDA:
        if elementos[1] == 1:
            return True
    elif acao == Acao.FRENTE:
        if elementos[4] == 1:
            return True
    elif acao == Acao.DIREITA:
        if elementos[7] == 1:
            return True
    return False

def estaFora(elementos,acao):
    if acao == Acao.ESQUERDA:
        if elementos[1] == -2:
            return True
    elif acao == Acao.FRENTE:
        if elementos[4] == -2:
            return True
    elif acao == Acao.DIREITA:
        if elementos[7] == -2:
            return True
    return False


