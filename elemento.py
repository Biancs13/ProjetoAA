class Elemento:
    def __init__(self,nome,pontos = 0, coletavel=False,solido=False):
        self.id = (int(coletavel),int(solido),pontos)
        self.nome = nome
        self.coletavel = coletavel
        self.solido = solido
        self.pontos = pontos

    def getId(self):
        return self.id

    def getName(self):
        return self.nome

    def isColetavel(self):
        return self.coletavel

    def isSolido(self):
        return self.solido

    def getPontos(self):
        return self.pontos
