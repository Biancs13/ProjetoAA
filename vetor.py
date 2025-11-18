from posicao import Posicao

class Vetor:
    def __init__(self, x,y):
        self.x = x
        self.y = y

    def soma(self,pos):
        x = pos.getX() + self.x
        y = pos.getY() + self.y
        return Posicao(x,y)
