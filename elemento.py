class Elemento:
    def __init__(self,nome,pontos = 0, coletavel=False,solido=False):
        self.id = (int(coletavel),int(solido),pontos)
        self.nome = nome
        print(f"nome: {self.nome} é solido: {solido} e coletavel: {coletavel} ")

    def getId(self):
        return self.id

    def getNome(self):
        return self.nome

    def isColetavel(self):
        return bool(self.id[0])

    def isSolido(self):
        return bool(self.id[1])

    def getPontos(self):
        return self.id[2]

    def __str__(self):
        return self.nome[0].upper()
