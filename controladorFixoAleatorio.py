
from controlador import Controlador

class ControladorFixoAleatorio(Controlador):

    def __init__(self, ficheiro_motor,problema,tempo,modo,aleatorio = False, repeticoes=1):
        super().__init__(ficheiro_motor,problema,tempo,modo)
        self.aleatorio = aleatorio
        self.acoes = []
        self.repeticoes = repeticoes
        self.numero_passos = []

    def executar_aprendizagem(self):
        for _ in range(self.repeticoes):
            if self.aleatorio == True:
                motor = self.criar_motor("aleatorio")
            else:
                motor = self.criar_motor("fixo")
            motor.executa()
            self.numero_passos.append(motor.agentes[0].num_passos)
        motor.agentes[0].escreverMelhor()



    def executar_teste(self):
        for _ in range(self.repeticoes):
            if self.aleatorio:
                motor = self.criar_motor("aleatorio")
            else:
                motor = self.criar_motor("fixo")
            motor.executa()



def criaFixoAleatorio(modo,problema,ficheiroMotor,aleatorio = False,repeticoes=1):
    problema = problema.split(" ")
    if problema[0] == "R":
        tempo = int(problema[1])
    else:
        tempo = None
    ficheiroMotor = ficheiroMotor[0].split(" ")[1]
    controlador = ControladorFixoAleatorio(ficheiroMotor,problema[0],tempo,modo,aleatorio,repeticoes)
    return controlador








