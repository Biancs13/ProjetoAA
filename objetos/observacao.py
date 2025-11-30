class Observacao:
    def __init__(self):
        self.elementos = [None,None,None]

    def adicionar(self, elemento, i):
        self.elementos[i] = elemento

    def getElementos(self):
        return self.elementos

    def __str__(self):
        return f"Elementos: {self.elementos}"