class Observacao:
    def __init__(self):
        self.elementos = {}

    def adicionar(self, vetor, elemento):
        if self.elementos[vetor] is not None:
            self.elementos[vetor] = elemento