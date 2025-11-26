import random
from abc import abstractmethod, ABC

from acao import *
from posicao import dentroLimites


class Agente(ABC):
    def __init__(self, id, posicaoAtual, angulo=0):
        self.id = id
        self.posicaoAtual = posicaoAtual
        self.angulo = angulo
        #self.politica = politica
        self.sensor = None
        self.coletaveis = []
        self.observavaoAtual = None

    def getId(self):
        return self.id

    def getPosicao(self):
        return self.posicaoAtual

    def getObservacao(self,obs):
        self.observavaoAtual = obs

    @abstractmethod
    def age(self):
        pass

    @abstractmethod
    def avaliacaoEstadoAtual(self,recompensa):
        pass

    def instala(self,sensor):
        if self.sensor is None:
            self.sensor = sensor
        else:
            self.sensor.getCampoVisao().append(sensor.getCampoVisao())

    def getSensor(self):
        return self.sensor

    #Não Altera o agente
    def ageAleatorio(self,maxGrid):
        while True:
            acao = getAcaoAleatoria()
            novaPos, novoAng = atuar(self, acao)
            if dentroLimites(novaPos, maxGrid):
                print(acao)
                return novaPos, novoAng
            #return novaPos,novoAng


    def rodar(self,novoAng):
        if self.sensor is not None:
            rotacao = (novoAng - self.angulo) % 360
            self.angulo = novoAng
            self.sensor.rodar(rotacao,novoAng)

    def coleta(self,elemento):
        if elemento.isColetavel():
            self.coletaveis.append(elemento)

    def getPontosColetaveis(self):
        pts = 0
        for c in self.coletaveis:
            pts += c.getPontos()
        return pts

    def alterar(self,novaPos,novoAng):
        self.rodar(novoAng)
        self.posicaoAtual = novaPos

    def __str__(self):
        return (f"Agente {self.id}: Posicao={self.posicaoAtual}, " f"Angulo={self.angulo}°")


def cria(ficheiro_agentes):
    # ["AG","1","(1,1)","0","F"]

    agentes_str = lerAgentes(ficheiro_agentes)
    agentes = []
    for ag in agentes_str:
        _, id, pos, ang, politica = ag

        x_str, y_str = pos.strip("()").split(',')
        posicao = Posicao(int(x_str), int(y_str))
        angulo = int(ang)
        agente = Agente(id, posicao, politica, angulo)
        agentes.append(agente)

    return agentes


def lerAgentes(ficheiro):
    fich = open(ficheiro, "r")
    linhas = fich.readlines()
    fich.close()

    agentesFich = []

    for linha in linhas:
        linha = linha.strip()
        if not linha or linha.startswith(";"):
            continue
        partes = linha.split()
        if partes[0] == "AG":
            agentesFich.append(partes)

    return agentesFich

def main():
    agentes = cria("agentes")
    for ag in agentes:
        print(ag)

if __name__ == "__main__":
    main()
