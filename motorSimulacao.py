from time import sleep

from agente import Agente
from ambiente import Ambiente
from posicao import Posicao
from elemento import Elemento
from sensor import Sensor
from vetor import Vetor


class MotorSimulacao:
    def __init__(self,ficheiro,modoAleatorio = True):
        self.ficheiro = ficheiro
        self.tamanhoGrelha = 0
        self.agentes = []
        #self.ambiente = Ambiente(tamanhoGrelha)
        self.tipo = ""
        self.modoAleatorio = modoAleatorio

    def cria(self,ficheiro):

        tipo,tempoLim, tamanhoGrelha, agentes, sensores, elementos = self.lerFicheiro(ficheiro)
        self.tipo = tipo.strip()
        self.tamanhoGrelha = int(tamanhoGrelha.strip())
        self.ambiente = Ambiente(self.tamanhoGrelha)
        for ag in agentes:
            _, id, pos, ang = ag
            x,y = pos.strip("()").split(',')
            posicao = Posicao(int(x),int(y))
            angulo = int(ang)

            agente = Agente(id,posicao,angulo)
            self.agentes.append(agente)

        #alterar de sítio
        def stringParaVetor(v_str):
            x_str, y_str = v_str.strip("()").split(',')
            return Vetor(int(x_str), int(y_str))

        for sen in sensores:
            _, idAg, vetor1, vetor2, vetor3 = sen #confirmar se é assim

            vetores = [vetor1,vetor2,vetor3]
            campoVisao = [stringParaVetor(v) for v in vetores]
            sensor = Sensor(campoVisao)

            for ag in self.agentes:
                if ag.id == idAg:
                    ag.instala(sensor)

        for ele in elementos:
            _, nome, pos, coletavel, solido = ele
            x,y = pos.strip("()").split(',')
            posicao = Posicao(int(x),int(y))

            elemento = Elemento(nome,posicao,bool(coletavel),bool(solido))
            self.ambiente.adicionar(elemento,posicao)

        return self

    def lerFicheiro(self,nome):
        fich = open(nome, "r")
        linhas = fich.readlines()
        fich.close()

        tipoFich = linhas[0]

        agentesFich = []
        sensoresFich = []
        elementosFich = []

        i = 1

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

        resultado = [tipoFich,tempoLim,tamanhoFich,agentesFich,sensoresFich,elementosFich]

        return resultado

    def verificaFicheiro(self,resultado):
        pass

    def listaAgentes(self):
        return self.agentes

    def executa(self):
        while not self.ambiente.condicaoFim(self.agentes):
            for agente in self.agentes:
                obs,pos = self.ambiente.observacaoParaAgente(agente)
                agente.observacao(obs)
                if (self.modoAleatorio):
                    novaPos, novoAng = agente.ageAleatorio(self.ambiente.tamanhoGrelha)
                else:
                    novaPos, novoAng = agente.age()
                ele = self.ambiente.getElemento(novaPos)
                if ele is None or not ele.isSolido():
                    agente.alterar(novaPos, novoAng)
                    if ele is not None and ele.isColetavel():
                        (agente.coleta(ele))
            print(self.representa())
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
