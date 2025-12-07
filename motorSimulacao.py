import os
from time import sleep

from agentes.agenteReforco import AgenteReforco
from objetos.acao import atuar
from agentes.agente import criaAgente
from ambientes.farol import Farol
from objetos.posicao import Posicao, dentroLimites
from objetos.elemento import Elemento
from ambientes.recolecao import Recolecao
from objetos.vetor import getDirecao


class MotorSimulacao:
    def __init__(self,modo,agentes,ambiente,tipo,num_passos):
        self.agentes = agentes
        self.ambiente = ambiente
        self.tipo = tipo #pode ser F ou R
        self.modo = modo #pode ser T ou A
        self.num_passos = num_passos

    def listaAgentes(self):
        return self.agentes

    def executa(self):
        i = 1
        if self.modo == "T":
            print(self.representa())
        self.inicializarObservacao()
        while not self.ambiente.condicaoFim(self.agentes) and i < self.num_passos * len(self.agentes):
            self.atualizarEstadoAgentes()
            for agente in self.agentes:
                acao = agente.age()
                novaPos, novoAng = atuar(agente, acao)
                pts =0
                if dentroLimites(novaPos,self.ambiente.tamanhoGrelha):
                    ele = self.ambiente.getElemento(novaPos)
                    if ele.getId() == (-1,-1,-1) or (ele != (-1,-1,-1) and not ele.isSolido()):
                        agente.alterar(novaPos, novoAng)
                        if ele.getId() != (-1,-1,-1) and ele.isColetavel():
                            (agente.coleta(ele))
                            self.ambiente.atualizacao(novaPos)
                        if ele.getId() != (-1,-1,-1) and self.tipo == "R" and ele.getNome() == "ninho":
                            pts = agente.getPontosColetaveis()
                            agente.recolher(pts)
                            self.ambiente.adicionarPontos(pts)
                        recompensa = self.ambiente.getRecompensa(novaPos, len(agente.coletaveis), pts)

                    else:
                        agente.num_colisoes +=1
                        recompensa = self.ambiente.getRecompensa(novaPos, len(agente.coletaveis), pts)

                else:
                    agente.num_colisoes += 1
                    recompensa = -80
                i +=1
                if isinstance(agente, AgenteReforco):
                    agente.avaliacaoEstadoAtual(recompensa)
            if self.modo == "T":
                print(self.representa(),"\n")
                sleep(0.5)
        if self.tipo != "R":
            for a in self.agentes:
                if self.ambiente.condicaoFim(self.agentes) :
                    a.condicaoFim = True


    def obterEstadoAtual(self):
        obs = self.ambiente.getObservacao(self.agentes)

    def atualizarEstadoAgentes(self):
        for agente in self.agentes:
            obs, pos = self.ambiente.observacaoParaAgente(agente)
            agente.observacao(obs)
            if self.tipo == "F":
                direcao1 = getDirecao(agente.posicaoAtual,self.ambiente.getPosicaoElementoMaisProximo(agente.posicaoAtual,"farol"))
                agente.atualizarEstadoAtual(direcao1)
            elif self.tipo == "R":
                direcao1 = getDirecao(agente.posicaoAtual,self.ambiente.getPosicaoElementoMaisProximo(agente.posicaoAtual,"ninho"))
                posOvo = self.ambiente.getPosicaoElementoMaisProximo(agente.posicaoAtual,"ovo")
                if posOvo is not None:
                    direcao2 = getDirecao(agente.posicaoAtual,posOvo)
                    agente.atualizarEstadoAtual(direcao1,direcao2)
                else:
                    agente.atualizarEstadoAtual(direcao1)

    def inicializarObservacao(self):
        for agente in self.agentes:
            obs,_ = self.ambiente.observacaoParaAgente(agente)
            agente.observacao(obs)

    def representa(self):
        pos_agentes = [a.getPosicao() for a in self.agentes]
        pos_vistas = [pos for a in self.agentes for pos in self.ambiente.observacaoParaAgente(a)[1] ]
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
                        linha.append("_")
                    elif elemento.getNome() == "Vazio":
                        linha.append(".")
                    else:
                        linha.append(str(elemento))
            linhas.append(" ".join(linha))
        return "\n".join(linhas)


def cria(ficheiro, tipo, politica,modo,tempo=0):
    tamanhoGrelha,numeroPassos, agentes_str, elementos_str = lerFicheiro(ficheiro)
    agentes = []
    if verificaFicheiro([tamanhoGrelha,numeroPassos, agentes_str,elementos_str]):
        if modo.strip() == "T":
            carregaMelhor = True
        else:
            carregaMelhor = False
        tamanhoGrelha = int(tamanhoGrelha.strip())
        if tipo == "R":
            ambiente = Recolecao(tamanhoGrelha,tempo)
        elif tipo == "F":
            ambiente = Farol(tamanhoGrelha)

        numeroPassos = int(numeroPassos.strip())

        for ag in agentes_str:
            path = "agentes/"+ag
            agentes.append(criaAgente(path,tamanhoGrelha,tipo,politica,numeroPassos,carregaMelhor))

        for ele in elementos_str:
            _, nome, pos, coletavel, solido, pts = ele
            x,y = pos.strip("()").split(',')
            posicao = Posicao(int(x),int(y))
            pts = int(pts.strip())
            solido_bool = True if solido == "True" else False
            coletavel_bool = True if coletavel == "True" else False
            elemento = Elemento(nome, pts, coletavel_bool, solido_bool)
            ambiente.adicionar(elemento,posicao)
        ms = MotorSimulacao(modo,agentes,ambiente,tipo,numeroPassos)
        return ms

def lerFicheiro(nome):
    fich = open(nome, "r")
    linhas = fich.readlines()
    fich.close()
    agentesFich = []
    sensoresFich = []
    elementosFich = []

    tamanhoFich = linhas[0]
    numeroPas = linhas[1]

    for linha in linhas[2:]:
        partes = linha.split()

        if partes[0] == "AG":
            agentesFich.append(partes[1])

        elif partes[0] == "S":
            sensoresFich.append(partes)

        elif partes[0] == "E":
            elementosFich.append(partes)

        else:
            pass

    resultado = [tamanhoFich,numeroPas,agentesFich,elementosFich]

    return resultado

def verificaFicheiro(resultado):
    tamanhoGrelha,numeroPas, agentesFich, elementos = resultado
    tamanho_grelha_int = int(tamanhoGrelha.strip())
    if tamanho_grelha_int < 3:
        return False
    elif type(tamanho_grelha_int) is not int:
        return False

    numeroPassos = int(numeroPas.strip())
    if numeroPassos < 10 or type(numeroPassos) is not int:
        return False

    for agenteFich in agentesFich:
        path = "agentes/" + agenteFich
        if not os.path.exists(path) or not os.path.isfile(path):
            return False

    def valida_coordenada(c_str):
        c = int(c_str)
        if c < 0 or c >= tamanho_grelha_int:
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

    for i, ele in enumerate(elementos):
        if len(ele) != 6:
            return False

        _, nome_str, pos_str, coletavel_str, solido_str,pts_str = ele

        valido = valida_posicao(pos_str)
        if not valido:
            return False

        if coletavel_str not in ['True', 'False']:
            return False
        if solido_str not in ['True', 'False']:
            return False
        pts = int(pts_str)
        if type(pts) is not int:
            return False
    return True


