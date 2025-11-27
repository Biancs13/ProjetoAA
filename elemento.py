class Elemento:
    def __init__(self,nome,pontos = 0, coletavel=False,solido=False):
        self.id = (int(coletavel),int(solido),pontos)
        self.nome = nome


    def getId(self):
        return self.id

    def getIdNormalizado(self):
        return(self.id[0],self.id[1],self.id[2]/100)

    def getNome(self):
        return self.nome

    def isColetavel(self):
        if self.id[0] == 1:
            return True
        else:
            return False

    def isSolido(self):
        if self.id[1] == 1:
            return True
        else:
            return False

    def getPontos(self):
        return self.id[2]

    def __str__(self):
        return self.nome[0].upper()
