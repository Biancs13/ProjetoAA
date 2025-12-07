from abc import ABC, abstractmethod


from motorSimulacao import cria

class Controlador(ABC):
    def __init__(self, ficheiro_motor, problema,tempo,modo):
        self.ficheiro_motor = ficheiro_motor
        self.problema = problema
        self.tempo = tempo
        self.modo = modo

    def criar_motor(self,politica):
        return cria(self.ficheiro_motor, self.problema, politica, self.modo,self.tempo)


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



def ler(nome):
    with open(nome, "r") as fich:
        return [linha.strip() for linha in fich.readlines()]


def criarControlador(ficheiro):
    from controladorGenetico import criaGenetico, ControladorGenetico
    from controladorReforco import criarReforco
    from controladorFixoAleatorio import criaFixoAleatorio


    conteudo = ler(ficheiro)
    modo = conteudo[0]
    problema = conteudo[1]
    politica = conteudo[2]
    if politica == "genetico":
        return criaGenetico(modo, problema, conteudo[3:])
    elif politica == "reforco":
        return criarReforco(modo, problema, conteudo[3:])
    elif politica == "fixo":
        return criaFixoAleatorio(modo,problema,conteudo[3:])
    else:
        return criaFixoAleatorio(modo,problema,conteudo[3:],True)



