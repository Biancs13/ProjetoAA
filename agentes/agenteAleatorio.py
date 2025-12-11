from objetos.acao import Acao,getAcaoAleatoria
from agentes.agente import Agente, escrever


class AgenteAleatorio(Agente):

    def __init__(self, id, posicaoInicial, tipo, angulo,ficheiro,treino = False):
        super().__init__(id,posicaoInicial,tipo, angulo,ficheiro)
        self.acoes = []
        self.treino = treino

    def age(self):
        if self.treino:
            acao = self.acoes.pop(0)
            return acao
        elementos = self.estadoAtual[1:10]
        while True:
            acao = getAcaoAleatoria()

            if estaFora(elementos,acao):
                continue

            if existeSolido(elementos,acao):
                continue

            self.acoes.append(acao)
            self.num_passos += 1
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


