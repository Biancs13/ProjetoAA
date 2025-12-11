from abc import abstractmethod, ABC
from typing import AbstractSet
from objetos.acao import *
from objetos.acao import Acao
from objetos.posicao import dentroLimites
from objetos.sensor import Sensor



class Agente(ABC):
    def __init__(self, id, posicaoAtual, tipoProblema, angulo,ficheiro):
        self.id = id
        self.num_passos = 0
        self.posicaoAtual = posicaoAtual
        self.angulo = angulo
        self.sensor = None
        self.coletaveis = []
        self.observacaoAtual = None
        self.estadoAtual = None
        self.tipoProblema = tipoProblema #Pode ser F ou R
        self.num_colisoes = 0
        self.num_pontos_recolhidos = 0
        self.condicaoFim = False
        self.ficheiro = ficheiro
        self.estadoAntigo = [] #Para o reforço, mas fica mais universal aqui

    def getId(self):
        return self.id

    def recolher(self,pontos):
        self.num_pontos_recolhidos += pontos
        self.coletaveis = []

    def getPosicao(self):
        return self.posicaoAtual

    def observacao(self,obs):
        self.observacaoAtual = obs

    def atualizarEstadoAtual(self,direcaoObj1,direcaoObj2 = None):
        novoEstado = []
        novoEstado.append(self.angulo/360) # o angulo fica em 0, 0.25, 0.5 ou 0.75 para indicar a orientação
        for elemento in self.observacaoAtual.getElementos():
            if elemento is None:
                novoEstado.extend([-1, 0, -1])
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
        if self.estadoAtual is None:
            self.estadoAntigo = novoEstado
        else:
            self.estadoAntigo = self.estadoAtual
        self.estadoAtual = novoEstado

    @abstractmethod
    def age(self):
        pass

    @abstractmethod
    def avaliacaoEstadoAtual(self,recompensa):
        pass

    @abstractmethod
    def escreverMelhor(self):
        pass

    def instala(self,sensor):
        if self.sensor is None:
            self.sensor = sensor
            if self.angulo != 0:
                sensor.rodar(self.angulo,self.angulo)
        else:
            if self.angulo != 0:
                sensor.rodar(self.angulo,self.angulo)
            self.sensor.getCampoVisao().extend(sensor.getCampoVisao())

    def getSensor(self):
        return self.sensor

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
        self.coletaveis = []
        return pts

    def alterar(self,novaPos,novoAng):
        self.rodar(novoAng)
        self.posicaoAtual = novaPos

    def getColetaveis(self):
        return self.coletaveis

    def __str__(self):
        return (f"Agente {self.id}: Posicao={self.posicaoAtual}, " f"Angulo={self.angulo}°")

def escrever(ficheiro,lista):
    fich = open(ficheiro,'r+')
    linhas = fich.readlines()
    primeiras = linhas[:4]
    fich.seek(0)
    for linha in primeiras:
        fich.write(linha)
    for i in lista:
        fich.write('\n' + str(i) )
    fich.truncate()

def lerFloats(lista):
    resultado = []
    for i in lista:
        resultado.append(float(i))
    return resultado

def lerAcoes(lista):
    acoes = []
    for acao in lista:
        acoes.append(Acao[acao.split(".")[-1]])
    return acoes

#Tirei para ser mais fácil
#alterar pq pode ser string
def valida(lista,tamanhoLista):
    if tamanhoLista != len(lista):
        return False
    return True

def criaAgente(ficheiro_agentes, tamanhoGrelha, tipoProblema, politica, passos, modo="A", carregarMelhor=False):
    from agentes.agenteFixo import AgenteFixo
    from agentes.agenteReforco import AgenteReforco, lerDicionario
    from agentes.agenteGenetico import AgenteGenetico
    from agentes.agenteAleatorio import AgenteAleatorio
    fich = open(ficheiro_agentes,"r")
    ag = [linha.strip() for linha in fich.readlines()]
    if(verificaFicheiro(ag,tamanhoGrelha)):
        id = int(ag[0])
        x_str, y_str = ag[1].strip("()").split(',')
        posicao = Posicao(int(x_str), int(y_str))
        angulo = int(ag[2])
        melhor = ag[4:]
        treino = (modo == "T")
        if politica == "fixo" :
            agente = AgenteFixo(id,posicao,tipoProblema, angulo,ficheiro_agentes,treino)
        if politica == "genetico":
            agente = AgenteGenetico(id,posicao,tipoProblema, angulo,ficheiro_agentes)
        if politica == "reforco":
            conteudo = ag[4:8]
            melhor = ag[8:]
            alpha,gama,epsilon_inicial,epsilon_final = conteudo
            alpha = float(alpha.strip())
            gama = float(gama.strip())
            epsilon_inicial = float(epsilon_inicial.strip())
            epsilon_final = float(epsilon_final.strip())
            agente = AgenteReforco(id, posicao, tipoProblema, angulo, ficheiro_agentes, alpha, gama, epsilon_inicial,
                                   epsilon_final)
        if politica == "aleatorio":
            agente = AgenteAleatorio(id,posicao,tipoProblema, angulo,ficheiro_agentes,treino)

        if carregarMelhor:
            if politica == "genetico":
                pesos = lerFloats(melhor)
                if pesos:
                    agente.pesos = pesos
            elif politica == "reforco":
                q = lerDicionario(ficheiro_agentes)
                if q:
                    agente.q = q
                    agente.epsilon = 0.0
            elif politica == "fixo" or politica == "aleatorio":
                acoes = lerAcoes(melhor)
                if acoes:
                    agente.acoes = acoes

        sen = ag[3].split()
        campoVisao =[]
        for v in sen[1:]:
            x, y = v.strip("()").split(',')
            campoVisao.append(Vetor(int(x), int(y)))
        sensor = Sensor(campoVisao)
        agente.instala(sensor)

        return agente


def verificaFicheiro(agente,tamanhoGrelha):
    id_str,pos,ang_str, sen = agente[0:4]
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


def estaFora(elementos,acao):
    if acao == Acao.ESQUERDA:
        if elementos[0] == -1 and elementos[1] == 0 and elementos[2] == -1:
            print("entrei")
            return True
    elif acao == Acao.FRENTE:
        if elementos[3] == -1 and elementos[4] == 0 and elementos[5] == -1:
            return True
    elif acao == Acao.DIREITA:
        if elementos[6] == -1 and elementos[7] == 0 and elementos[8] == -1:
            return True
    return False

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

