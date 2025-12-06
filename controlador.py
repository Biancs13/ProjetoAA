from abc import ABC, abstractmethod
from motorSimulacao import cria

class Controlador(ABC):
    def __init__(self, ficheiro_motor, problema,tempo,modo):
        self.ficheiro_motor = ficheiro_motor
        self.problema = problema
        self.tempo = tempo
        self.modo = modo

    def criar_motor(self,politica):
        return cria(self.ficheiro_motor, self.problema, politica,self.modo,self.tempo)


    def executar(self):
        if self.modo == 'A':
            self.executar_aprendizagem()
        if self.modo == 'T':
            self.executar_teste()

    @abstractmethod
    def executar_aprendizagem(self):
        pass

    @abstractmethod
    def executar_teste(self):
        pass

#adaptar quando se tiver Reforço feito
def criarControlador(ficheiro):
    from controladorGenetico import criaGenetico
    tipo_politica = ler(ficheiro)
    if tipo_politica == "genetico":
        return criaGenetico(ficheiro)
    return None
'''  
    if tipo_politica == "reforco":
        return criaReforco(ficheiro)
'''

def ler(ficheiro):
    fich = open(ficheiro, "r")
    linhas = fich.readlines()
    fich.close()
    return linhas[1].strip()