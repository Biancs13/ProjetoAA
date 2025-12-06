from controlador import Controlador

class ControladorReforco(Controlador):

    def __init__(self,episodios,ficheiro_motor,problema,modo,tempo=0):
        self.episodios = episodios
        super().__init__(ficheiro_motor, problema,modo,tempo)


    def executar_aprendizagem(self):
        q = {}
        for i in range(self.episodios):
            motor = self.criar_motor("reforco")
            motor.agentes[0].q = q
            motor.executa() # aqui treinamos
            q = motor.agentes[0].q
            print(i,q)
            motor.agentes[0].escreverDicionario(q)
        # TODO pôr aqui para guardar o melhor individuo

    def executar_teste(self):
        motor = self.criar_motor("reforco")

        motor.executa()


def get_max_recompensa_q(q):
    max_val = 0
    for estado, dic_acoes in q.items():
        if dic_acoes:
            max_val = max(max_val, max(dic_acoes.values()))
    return max_val



    