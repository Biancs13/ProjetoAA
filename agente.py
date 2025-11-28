import random
from abc import abstractmethod, ABC
from acao import *
from posicao import dentroLimites
from sensor import Sensor


class Agente(ABC):
    def __init__(self, id, posicaoAtual, tipoProblema, angulo):
        self.id = id
        self.posicaoAtual = posicaoAtual
        self.angulo = angulo
        #self.politica = politica
        self.sensor = None
        self.coletaveis = []
        self.observacaoAtual = None
        self.estadoAtual = None
        self.tipoProblema = tipoProblema #Pode ser F ou R

    def getId(self):
        return self.id

    def getPosicao(self):
        return self.posicaoAtual

    def observacao(self,obs):
        self.observacaoAtual = obs

    def atualizarEstadoAtual(self,direcaoObj1,direcaoObj2 = None):
        novoEstado = []
        novoEstado.append(self.angulo/360)# o angulo fica em 0, 0.25, 0.5 ou 0.75 para indicar a orientação
        print(self.observacaoAtual)
        for elemento in self.observacaoAtual.getElementos():
            if elemento is None:
                novoEstado.extend([-2, -2, -2])
            else:
                novoEstado.extend(elemento)
        if self.tipoProblema == "F":
            novoEstado.append(direcaoObj1.x)
            novoEstado.append(direcaoObj1.y)
            self.estadoAtual = novoEstado
        elif self.tipoProblema == "R":
            novoEstado.append(len(self.coletaveis)/100)
            novoEstado.append(direcaoObj1.x)
            novoEstado.append(direcaoObj1.y)
            if direcaoObj2 is not None:
                novoEstado.append(direcaoObj2.x)
                novoEstado.append(direcaoObj2.y)
            else:
                novoEstado.append(-1)
                novoEstado.append(-1)
            self.estadoAtual = novoEstado
        print(self.sensor)

    @abstractmethod
    def age(self):
        pass

    @abstractmethod
    def avaliacaoEstadoAtual(self,recompensa):
        pass

    def instala(self,sensor):
        if self.sensor is None:
            self.sensor = sensor
            if self.angulo != 0:
                sensor.rodar(self.angulo,self.angulo)
        else:
            if self.angulo != 0:
                sensor.rodar(self.angulo,self.angulo)
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

def cria(ficheiro_agentes,tamanhoGrelha):
    from agenteAleatorio import AgenteAleatorio
    from agenteFixo import AgenteFixo
    from agenteGenetico import AgenteGenetico
    from agenteReforco import AgenteReforco
    fich = open(ficheiro_agentes,"r")
    ag = [linha.strip() for linha in fich.readlines()]
    if(verificaFicheiro(ag,tamanhoGrelha)):
        id = int(ag[0])
        x_str, y_str = ag[1].strip("()").split(',')
        posicao = Posicao(int(x_str), int(y_str))
        politica = ag[2]
        angulo = int(ag[3])

        if politica == "fixo" :
            agente = AgenteFixo(id, posicao, politica, angulo)
        if politica == "genetico":
            agente = AgenteGenetico(id, posicao, angulo)
        if politica == "reforco":
            agente = AgenteReforco(id, posicao, angulo)
        if politica == "aleatorio":
            agente = AgenteAleatorio(id, posicao, angulo)

        sen = ag[4].split()
        campoVisao =[]
        for v in sen[1:]:
            x, y = v.strip("()").split(',')
            campoVisao.append(Vetor(int(x), int(y)))
        sensor = Sensor(campoVisao)
        agente.instala(sensor)

        return agente


def verificaFicheiro(agente,tamanhoGrelha):
    id_str,pos,politica,ang_str, sen = agente
    id = int(id_str)
    if type(id) is not int or id < 0:
        return False

    def valida_coordenada(c_str):
        c = int(c_str)
        if c < 0 or c >= tamanhoGrelha:
            return False,None
        elif type(c) is not int:
            return False,None
        return True, c

    def valida_posicao(pos_str):
        if not (pos_str.startswith('(') and pos_str.endswith(')') and ',' in pos_str):
            return False
        x_str, y_str = pos_str.strip("()").split(',')
        val_x, res_x = valida_coordenada(x_str.strip())
        val_y, res_y = valida_coordenada(y_str.strip())

        if not val_x:
            return False
        if not val_y:
            return False
        return True

    valido = valida_posicao(pos)
    if not valido:
        return False

    if politica not in ["fixo","genetico","reforco","aleatorio"]:
        return False

    ang = int(ang_str)
    if type(ang) is not int or ang not in [0,90,270,360]:
        return False

    sensor = sen.split();
    if not sensor[0] == "S":
        return False

    if len(sensor) < 2:
        return False

    def valida_vetor(v_str):
        if not (v_str.startswith('(') and v_str.endswith(')') and ',' in v_str):
            return False
        x_str, y_str = v_str.strip("()").split(',')
        x_int = int(x_str.strip())
        y_int = int(y_str.strip())
        if type(x_int) is not int or type(y_int) is not int:
            return False
        return True

    for v in sensor[1:]:
        if not valida_vetor(v):
            return False

    return True


# No final do ficheiro agente.py, substitua ou adapte o bloco main:

def main():
    tamanho_da_grelha = 10
    agente = cria("agentes", tamanho_da_grelha)
    if agente:
        print(" Criação do Agente SUCESSO:")
        print(agente)

        sensor = agente.getSensor()
        if sensor:
            campo_visao_str = [str(v) for v in sensor.getCampoVisao()]
            print(f"   - Campo de Visão: {campo_visao_str}")
        else:
            print("   - Sensor: Nenhum sensor instalado.")

    else:
        print(" Criação do Agente FALHOU.")


if __name__ == "__main__":
    main()
