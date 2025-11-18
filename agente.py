import random


class Agent:
    def __init__(self, id, posicao):
        self.id = id
        self.posicao = posicao
    
    def move(self, novaPosicao):
        self.posicao = novaPosicao
    
    def randomMove(self, tamanhoGrelha):
        pass
    

    def getPosicao(self):
        return self.posicao
    
    def getId(self):
        return self.id
    

#so um teste