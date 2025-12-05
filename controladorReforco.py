from motorSimulacao import cria


class ControladorReforco():


    def __init__(self,episodios,ficheiro_motor,problema,tempo=0):
        self.episodios = episodios
        self.ficheiro_motor = ficheiro_motor
        self.problema = problema
        self.tempo = tempo


    def executar(self):
        q = {}
        for i in range(self.episodios):
            motor = cria(self.ficheiro_motor,self.problema,"reforco",self.tempo)
            motor.agentes[0].q = q
            motor.executa() # aqui treinamos
            q = motor.agentes[0].q
            print(i,q)

        # TODO pôr aqui para guardar o melhor individuo


def get_max_recompensa_q(q):
    max_val = 0
    for estado, dic_acoes in q.items():
        if dic_acoes:
            max_val = max(max_val, max(dic_acoes.values()))
    return max_val



    