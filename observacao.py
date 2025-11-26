class Observacao:
    def __init__(self,):
        self.elementos = [None,None,None]

    def adicionar(self, elemento, i):
        if elemento is not None:
            self.elementos[i] = elemento
