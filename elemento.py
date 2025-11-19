class Elemento:
    def __init__(self,nome,pontos = 0, coletavel=False,solido=False):
        self.id = (int(coletavel),int(solido),pontos)
        self.nome = nome

    def getId(self):
        return self.id

    def getName(self):
        return self.nome

    def isColetavel(self):
        return bool(self.id[0])

    def isSolido(self):
        return bool(self.id[1])

    def getPontos(self):
        return self.id[2]
