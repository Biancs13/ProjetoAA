from time import sleep

from ambiente import Ambiente
from posicao import Posicao


class MotorSimulacao:
    def __init__(self,ficheiro,modoAleatorio = True):
        tamanhoGrelha = 0
        self.agentes = []
        self.ambiente = Ambiente(tamanhoGrelha)
        self.tipo = "F" # "R"
        self.modoAleatorio = modoAleatorio

    def getAgentes(self):
        return self.agentes

    def executa(self):
        print(self.representa())
        while not self.ambiente.condicaoFim(self.agentes):
            for agente in self.agentes:
                obs,pos = self.ambiente.observacaoParaAgente(agente)
                agente.observacao(obs)
                if (self.modoAleatorio):
                    novaPos, novoAng = agente.ageAleatorio(self.ambiente.tamanhoGrelha)
                else:
                    novaPos, novoAng = agente.age()
                ele = self.ambiente.getElemento(novaPos)
                if not ele.isSolido():
                    agente.alterar(novaPos, novoAng)
                    if ele.isColetavel():
                        (agente.coleta(ele))
            sleep(1) #Quando queremos testar


    def representa(self):
        pos_agentes = [a.getPosicao() for a in self.agentes]
        pos_vistas = [self.ambiente.observacaoParaAgente(a)[1] for a in self.agentes]
        linhas = []
        for y in range(self.ambiente.tamanhoGrelha):
            linha = []
            for x in range(self.ambiente.tamanhoGrelha):
                if Posicao(x, y) in pos_agentes:
                    linha.append("A")
                elif Posicao(x, y) in pos_vistas:
                    linha.append("*")
                else:
                    elemento = self.ambiente.getElemento(Posicao(x, y))
                    if elemento is None:
                        linha.append(".")
                    else:
                        linha.append(str(elemento))
            linhas.append(" ".join(linha))
        return "\n".join(linhas)


if __name__ == "__main__":
    motorSimulacao = MotorSimulacao(None)
    motorSimulacao.executa()
