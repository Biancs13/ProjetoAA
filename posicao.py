class Posicao:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def equals(self,other):
        return self.x == other.x and self.y == other.y