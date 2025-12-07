
from controlador import Controlador



class ControladorFixoAleatorio(Controlador):

    def __init__(self, ficheiro_motor,problema,tempo,modo,aleatorio = False):
        super().__init__(ficheiro_motor,problema,tempo,modo)
        self.aleatorio = aleatorio
        self.acoes =  []

    def executar_aprendizagem(self):
        if self.aleatorio:
            motor = self.criar_motor("aleatorio")
        else:
            motor = self.criar_motor("fixo")
        motor.executa()
        motor.agentes[0].escreverMelhor()


    def executar_teste(self):
        if self.aleatorio:
            motor = self.criar_motor("aleatorio")
        else:
            motor = self.criar_motor("fixo")
        motor.executa()



def criaFixoAleatorio(modo,problema,ficheiroMotor,aleatorio = False):
    problema = problema.split(" ")
    if problema[0] == "R":
        tempo = int(problema[1])
    else:
        tempo = None
    ficheiroMotor = ficheiroMotor[0].split(" ")[1]
    controlador = ControladorFixoAleatorio(ficheiroMotor,problema[0],tempo,modo,aleatorio)
    return controlador








