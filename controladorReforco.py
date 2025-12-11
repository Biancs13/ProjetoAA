from controlador import Controlador
from objetos.acao import atuar


class ControladorReforco(Controlador):

    def __init__(self,episodios,ficheiro_motor,problema,modo,tempo=0):
        self.episodios = episodios
        self.melhores_recompensas_ep =[]
        self.numero_passos = []
        super().__init__(ficheiro_motor, problema,tempo,modo)


    def executar_aprendizagem(self):
        q = {}
        epsilon = 0
        lista_passos_100 = []

        for ep in range(self.episodios + 1):

            motor = self.criar_motor("reforco", self.episodios)
            agente = motor.agentes[0]

            agente.q = q
            if epsilon != 0:
                agente.epsilon = epsilon

            motor.executa()

            agente.atualizar_epsilon(ep)
            q = agente.q
            epsilon = agente.epsilon
            lista_passos_100.append(agente.num_passos)

            if ep % 100 == 0:
                self.melhores_recompensas_ep.append(get_max_recompensa_q(q))
                melhor = max(lista_passos_100)
                self.numero_passos.append(melhor)
                lista_passos_100 = []

            if ep % 1000 == 0:
                print(f"Episódio: {ep}/{self.episodios} | Max R:", get_max_recompensa_q(q))
        motor = self.criar_motor("reforco", self.episodios)
        motor.agentes[0].q = q
        motor.agentes[0].escreverMelhor()



    def executar_teste(self):
        motor = self.criar_motor("reforco", self.episodios)
        motor.executa()




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
