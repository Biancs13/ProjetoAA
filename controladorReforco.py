from controlador import Controlador
from objetos.acao import atuar


class ControladorReforco(Controlador):

    def __init__(self,episodios,ficheiro_motor,problema,modo,tempo=0):
        super().__init__(ficheiro_motor, problema,tempo,modo)
        self.episodios = episodios
        motor_temp = self.criar_motor("reforco", self.episodios)
        self.melhores_recompensas_ep = {agente.id:[] for agente in motor_temp.agentes}
        self.numero_passos = {agente.id:[] for agente in motor_temp.agentes}
        #self.epsillon = []
        self.melhores_caminhos = {agente.id:[] for agente in motor_temp.agentes}


    def executar_aprendizagem(self):
        motor_temp = self.criar_motor("reforco", self.episodios)

        todos_q = {agente.id: None for agente in motor_temp.agentes}
        todos_epsilon = {agente.id: None for agente in motor_temp.agentes}
        todos_estados_visitas = {agente.id: None for agente in motor_temp.agentes}

        lista_passos_100 = {agente.id:[] for agente in motor_temp.agentes}

        for ep in range(self.episodios + 1):
            motor = self.criar_motor("reforco", self.episodios)
            for agente in motor.agentes:
                if todos_estados_visitas[agente.id] is not None:
                    agente.estado_visitas = todos_estados_visitas[agente.id]
                if todos_q[agente.id] is not None:
                    agente.q = todos_q[agente.id]
                if todos_epsilon[agente.id] is not None:
                    agente.epsilon = todos_epsilon[agente.id]

            motor.executa()

            for agente in motor.agentes:
                agente.atualizar_epsilon(ep)
                todos_q[agente.id] = agente.q
                todos_estados_visitas[agente.id] = agente.estado_visitas
                todos_epsilon[agente.id] = agente.epsilon
                lista_passos_100[agente.id].append(agente.num_passos)

            if ep % 100 == 0:
                for agente in motor.agentes:
                    if lista_passos_100[agente.id]:
                        self.melhores_recompensas_ep[agente.id].append(get_max_recompensa_q(todos_q[agente.id]))
                        self.numero_passos[agente.id].append(min(lista_passos_100[agente.id]))
                        lista_passos_100[agente.id] = []
            if  ep % 1000 == 0:
                max_r_todos_agentes = []
                for agente in motor.agentes:
                    max_r_todos_agentes.append(get_max_recompensa_q(todos_q[agente.id]))
                print(f"Episódio: {ep}/{self.episodios} | Max R:", max(max_r_todos_agentes))
        motor = self.criar_motor("reforco", self.episodios)
        for agente in motor.agentes:
            agente.q = todos_q[agente.id]
            agente.escreverMelhor()



    def executar_teste(self,showGUI = True):
        motor = self.criar_motor("reforco", self.episodios)
        motor.executa(showGUI)
        for agente in motor.agentes:
            self.melhores_caminhos[agente.id].append(agente.comportamento)



def get_max_recompensa_q(q):
    max_val = 0
    for estado, dic_acoes in q.items():
        if dic_acoes:
            max_val = max(max_val, max(dic_acoes.values()))
    return max_val

def criarReforco(modo,problema,conteudo):
    episodios,ficheiro_motor = conteudo
    episodios = int(episodios.strip())
    ficheiro_motor = ficheiro_motor.split(" ")[1]
    problema = problema.split(" ")
    if problema[0] == "R":
        tempo = int(problema[1])
    else:
        tempo = None
    return ControladorReforco(episodios,ficheiro_motor,problema[0],modo,tempo)
