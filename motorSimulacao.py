from time import sleep

from AgenteFixo import AgenteFixo
from agente import Agente
from ambiente import Ambiente
from farol import Farol
from posicao import Posicao, dentroLimites
from elemento import Elemento
from recolecao import Recolecao
from sensor import Sensor
from vetor import Vetor

class MotorSimulacao:
    def __init__(self,modo,agentes,ambiente,tipo):
        print("entrei construtor")
        self.agentes = agentes
        self.ambiente = ambiente
        self.tipo = tipo #pode ser F ou R
        self.modo = modo #pode ser T ou A

    def listaAgentes(self):
        return self.agentes

    def executa(self):
        print(self.representa())
        while not self.ambiente.condicaoFim(self.agentes):
            for agente in self.agentes:
                obs,pos = self.ambiente.observacaoParaAgente(agente)
                agente.getObservacao(obs)
                novaPos, novoAng = agente.ageAleatorio(self.ambiente.tamanhoGrelha)
                if dentroLimites(novaPos,self.ambiente.tamanhoGrelha):
                    ele = self.ambiente.getElemento(novaPos)
                    if ele is None or (ele is not None and not ele.isSolido()):
                        agente.alterar(novaPos, novoAng)
                        if ele is not None and ele.isColetavel():
                            (agente.coleta(ele))
                            self.ambiente.atualizacao(novaPos)
                        if ele is not None and self.tipo == "R" and ele.getNome() == "ninho":
                            pts = agente.getPontosColetaveis()
                            self.ambiente.recolher(pts)
            print(self.representa())
            sleep(0.5) #Quando queremos testar

    def obterEstadoAtual(self):
        obs = self.ambiente.getObservacao(self.agentes)


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
                        linha.append(".")
                    else:
                        linha.append(str(elemento))
            linhas.append(" ".join(linha))
        return "\n".join(linhas)

def cria(ficheiro):
    modo,tipo,tempoLim, tamanhoGrelha, agentes_str, sensores, elementos_str = lerFicheiro(ficheiro)
    agentes = []
    print(verificaFicheiro([modo,tipo,tempoLim, tamanhoGrelha, agentes, sensores, elementos_str]))
    if verificaFicheiro([modo,tipo,tempoLim, tamanhoGrelha, agentes_str, sensores, elementos_str]):
        tamanhoGrelha = int(tamanhoGrelha.strip())
        tipo = tipo.strip()
        if tipo == "R":
            ambiente = Recolecao(tamanhoGrelha,int(tempoLim))
        elif tipo == "F":
            ambiente = Farol(tamanhoGrelha)
        modo = modo.strip()
        for ag in agentes_str:
            _, id, pos, ang = ag
            x,y = pos.strip("()").split(',')
            posicao = Posicao(int(x),int(y))
            angulo = int(ang)
            agente = AgenteFixo(id,posicao,tipo,angulo)
            agentes.append(agente)

        #alterar de sítio
        def stringParaVetor(v_str):
            x_str, y_str = v_str.strip("()").split(',')
            return Vetor(int(x_str), int(y_str))

        for sen in sensores:
            _, idAg, vetor1, vetor2, vetor3 = sen #confirmar se é assim

            vetores = [vetor1,vetor2,vetor3]
            campoVisao = [stringParaVetor(v) for v in vetores]
            sensor = Sensor(campoVisao)

            for ag in agentes:
                if ag.id == idAg:
                    ag.instala(sensor)

        for ele in elementos_str:
            _, nome, pos, coletavel, solido, pts = ele
            x,y = pos.strip("()").split(',')
            posicao = Posicao(int(x),int(y))
            pts = int(pts.strip())
            solido_bool = True if solido == "True" else False
            coletavel_bool = True if coletavel == "True" else False
            elemento = Elemento(nome, pts, coletavel_bool, solido_bool)
            ambiente.adicionar(elemento,posicao)
        ms = MotorSimulacao(modo,agentes,ambiente,tipo)
        print(type(ms))
        print("MS:",ms)
        return ms

def lerFicheiro(nome):
    fich = open(nome, "r")
    linhas = fich.readlines()
    fich.close()

    modoFich = linhas[0]
    tipoFich = linhas[1]

    agentesFich = []
    sensoresFich = []
    elementosFich = []

    i = 2
    tipoFich = linhas[1].strip()
    if tipoFich == "R":
        tempoLim = linhas[i]
        i += 1
    else:
        tempoLim = None

    tamanhoFich = linhas[i]
    i += 1

    for linha in linhas[i:]:
        partes = linha.split()

        if partes[0] == "AG":
            agentesFich.append(partes)

        elif partes[0] == "S":
            sensoresFich.append(partes)

        elif partes[0] == "E":
            elementosFich.append(partes)

        else:
            pass

    resultado = [modoFich,tipoFich,tempoLim,tamanhoFich,agentesFich,sensoresFich,elementosFich]

    return resultado

def verificaFicheiro(resultado):
    modo,tipo, tempoLim, tamanhoGrelha, agentes, sensores, elementos = resultado

    modo = modo.strip()
    if modo not in ["A", "T"]:
        return False

    tipo = tipo.strip()
    if tipo not in ["R", "F"]:
        return False

    tamanho_grelha_int = int(tamanhoGrelha.strip())
    if tamanho_grelha_int < 3:
        return False
    elif type(tamanho_grelha_int) is not int:
        return False

    if tipo == "R":
        limite = int(tempoLim.strip())
        if limite <= 10:
            return False
        elif type(limite) is not int:
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

    if not agentes:
        return False

    agente_ids = set()
    for i, ag in enumerate(agentes):
        if len(ag) != 4:
            return False

        _, id_str, pos_str, ang_str = ag

        agente_id = int(id_str)
        if agente_id in agente_ids:
            return False
        elif type(agente_id) is not int:
            return False
        agente_ids.add(agente_id)

        valido = valida_posicao(pos_str)
        if not valido:
            return False
        ang_int =int(ang_str)
        if type(ang_int) is not int:
            return False

    for i, sen in enumerate(sensores):
        if len(sen) != 5:
            return False

        _, idAg_str, v1_str, v2_str, v3_str = sen

        idAg = int(idAg_str)
        if idAg not in agente_ids:
            return False
        elif type(idAg) is not int:
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

        for j, v_str in enumerate([v1_str, v2_str, v3_str]):
            valido = valida_vetor(v_str)
            if not valido:
                return False

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


