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
        if self.verificaFicheiro([tipo,tempoLim, tamanhoGrelha, agentes, sensores, elementos]):
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

    def verificaFicheiro(self, resultado):
        tipo, tempoLim, tamanhoGrelha, agentes, sensores, elementos = resultado

        tipo = tipo.strip()
        if tipo not in ["R", "F"]:
            print(f"Erro de Tipo: Tipo de ficheiro inválido: '{tipo}'. Deve ser 'R' (Regressivo) ou 'F' (Fim).")
            return False

        try:
            tamanho_grelha_int = int(tamanhoGrelha.strip())
            if tamanho_grelha_int < 3:
                print(f"Erro de Tamanho: O tamanho da grelha deve ser um inteiro positivo e maior ou igual a 3, mas é '{tamanho_grelha_int}'.")
                return False
        except ValueError:
            print(f"Erro de Tamanho: O tamanho da grelha ('{tamanhoGrelha.strip()}') não é um número inteiro válido.")
            return False

        if tipo == "R":
            try:
                limite = int(tempoLim.strip())
                if limite <= 0:
                    print(f" Erro de Tempo Limite: O tempo limite deve ser um inteiro positivo, mas é '{limite}'.")
                    return False
            except ValueError:
                print(f"Erro de Tempo Limite: O tempo limite ('{tempoLim.strip()}') não é um número inteiro válido.")
                return False

        def valida_coordenada(c_str, nome_campo):
            try:
                c = int(c_str)
                if c < 0 or c >= tamanho_grelha_int:
                    return False, f"{nome_campo} ('{c}') fora do limite da grelha [0, {tamanho_grelha_int - 1}]."
                return True, c
            except ValueError:
                return False, f"{nome_campo} ('{c_str}') não é um inteiro válido."

        def valida_posicao(pos_str, nome_entidade, entidade_id_ou_nome):
            if not (pos_str.startswith('(') and pos_str.endswith(')') and ',' in pos_str):
                 return False, f"Posição de {nome_entidade} '{entidade_id_ou_nome}' ('{pos_str}') não está no formato '(x,y)'."

            try:
                x_str, y_str = pos_str.strip("()").split(',')
                val_x, res_x = valida_coordenada(x_str.strip(), "Coordenada X")
                val_y, res_y = valida_coordenada(y_str.strip(), "Coordenada Y")

                if not val_x:
                    return False, f"Erro de Posição em {nome_entidade} '{entidade_id_ou_nome}': {res_x}"
                if not val_y:
                    return False, f"Erro de Posição em {nome_entidade} '{entidade_id_ou_nome}': {res_y}"
                return True, None
            except:
                return False, f"Erro de Posição em {nome_entidade} '{entidade_id_ou_nome}': Falha ao analisar as coordenadas."

        if not agentes:
            print("Erro de Agentes: O ficheiro deve definir pelo menos um agente (AG).")
            return False

        agente_ids = set()
        for i, ag in enumerate(agentes):
            if len(ag) != 4:
                print(f" Erro de Formato AG (linha {i+1}): 'AG' deve ter 4 campos. Encontrado: {ag}")
                return False

            _, id_str, pos_str, ang_str = ag

            try:
                agente_id = int(id_str)
                if agente_id in agente_ids:
                    print(f" Erro de ID: ID de agente duplicado: '{agente_id}'.")
                    return False
                agente_ids.add(agente_id)
            except ValueError:
                print(f" Erro de ID: ID do agente ('{id_str}') não é um inteiro válido.")
                return False

            valido, erro_msg = valida_posicao(pos_str, "Agente", id_str)
            if not valido:
                print(f" {erro_msg}")
                return False

            try:
                int(ang_str)
            except ValueError:
                print(f" Erro de Ângulo: Ângulo do agente '{id_str}' ('{ang_str}') não é um inteiro válido.")
                return False

        for i, sen in enumerate(sensores):
            if len(sen) != 5:
                print(f" Erro de Formato S (linha {i+1}): 'S' deve ter 5 campos. Encontrado: {sen}")
                return False

            _, idAg_str, v1_str, v2_str, v3_str = sen

            try:
                idAg = int(idAg_str)
                if idAg not in agente_ids:
                    print(f" Erro de Consistência: Sensor referencia Agente ID '{idAg}' que não está definido.")
                    return False
            except ValueError:
                print(f" Erro de ID: ID do Agente no Sensor ('{idAg_str}') não é um inteiro válido.")
                return False

            def valida_vetor(v_str, vetor_nome):
                if not (v_str.startswith('(') and v_str.endswith(')') and ',' in v_str):
                    return False, f"Vetor {vetor_nome} do sensor do Agente '{idAg_str}' ('{v_str}') não está no formato '(dx,dy)'."
                try:
                    x_str, y_str = v_str.strip("()").split(',')
                    int(x_str.strip())
                    int(y_str.strip())
                    return True, None
                except ValueError:
                    return False, f"Coordenadas do Vetor {vetor_nome} do Agente '{idAg_str}' ('{v_str}') não são inteiros válidos."

            for j, v_str in enumerate([v1_str, v2_str, v3_str]):
                valido, erro_msg = valida_vetor(v_str, f"Vetor {j+1}")
                if not valido:
                    print(f" Erro de Formato de Vetor: {erro_msg}")
                    return False

        for i, ele in enumerate(elementos):
            if len(ele) != 5:
                print(f" Erro de Formato E (linha {i+1}): 'E' deve ter 5 campos. Encontrado: {ele}")
                return False

            _, nome_str, pos_str, coletavel_str, solido_str = ele

            valido, erro_msg = valida_posicao(pos_str, "Elemento", nome_str)
            if not valido:
                print(f" {erro_msg}")
                return False

            if coletavel_str not in ['True', 'False']:
                print(f" Erro de Tipo: O campo 'coletavel' do Elemento '{nome_str}' ('{coletavel_str}') deve ser 'True' ou 'False'.")
                return False
            if solido_str not in ['True', 'False']:
                print(f" Erro de Tipo: O campo 'solido' do Elemento '{nome_str}' ('{solido_str}') deve ser 'True' ou 'False'.")
                return False

        return True

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
