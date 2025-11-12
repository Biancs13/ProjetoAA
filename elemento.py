class Elemento:
    def __init__(self,nome,coletavel=False,solido=False):
        self.nome = nome
        self.coletavel = coletavel
        self.solido = solido

    def getName(self):
        return self.nome

    def isColetavel(self):
        return self.coletavel

    def isSolido(self):
        return self.solido