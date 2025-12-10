from controlador import Controlador
from objetos.acao import atuar


class ControladorReforco(Controlador):

    def __init__(self,episodios,ficheiro_motor,problema,modo,tempo=0):
        self.episodios = episodios
        self.melhores_recompensas_ep =[]
        super().__init__(ficheiro_motor, problema,tempo,modo)


    def executar_aprendizagem(self):
        q = {}
        for i in range(self.episodios +1):
            motor = self.criar_motor("reforco")
            motor.agentes[0].q = q
            motor.executa() # aqui treinamos
            q = motor.agentes[0].q
            if i % 100 == 0:
                self.melhores_recompensas_ep.append(get_max_recompensa_q(q))
            if i % 1000 == 0:
                print(f"Episódio: {i}/{self.episodios}: Recompensa máxima encontrada:",get_max_recompensa_q(q))
        motor = self.criar_motor("reforco")
        motor.agentes[0].q = q
        motor.agentes[0].escreverMelhor()


    def executar_teste(self):
        motor = self.criar_motor("reforco")
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

#Para os gráficos
def reconstruir_caminho(posicao,angulo, comportamento):
    caminho = []
    for a in comportamento:
        novaPos, novaAng = atuar(posicao,angulo,a)
        caminho.append(posicao)
        posicao = novaPos
        angulo = novaAng
    return caminho