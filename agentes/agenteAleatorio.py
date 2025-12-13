from objetos.acao import Acao,getAcaoAleatoria
from agentes.agente import Agente, escrever, estaFora, existeSolido


class AgenteAleatorio(Agente):

    def __init__(self, id, posicaoInicial, tipo, angulo,ficheiro,treino = False):
        super().__init__(id,posicaoInicial,tipo, angulo,ficheiro)
        self.acoes = []
        self.treino = treino

    def age(self):
        if self.treino:
            acao = self.acoes.pop(0)
            return acao
        elementos = self.estadoAtual[0:9]
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



