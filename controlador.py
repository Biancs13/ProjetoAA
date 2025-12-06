from abc import ABC, abstractmethod

from controladorGenetico import criaGenetico
from motorSimulacao import cria

class Controlador(ABC):
    def __init__(self, ficheiro_motor, problema,tempo):
        self.ficheiro_motor = ficheiro_motor
        self.problema = problema
        self.tempo = tempo

    def criar_motor(self,tipo):
        return cria(self.ficheiro_motor, self.problema, tipo, self.tempo)

    @abstractmethod
    def executar(self):
        pass

#adaptar quando se tiver Reforço feito
def criarControlador(ficheiro):
    tipo_politica = ler(ficheiro)
    if tipo_politica == "genetico":
        return criaGenetico(ficheiro)
'''  
    if tipo_politica == "reforco":
        return criaReforco(ficheiro)
'''

def ler(ficheiro):
    fich = open(ficheiro, "r")
    linhas = fich.readlines()
    fich.close()
    return linhas[1].strip()