class Posicao:
    def __init__(self,x,y,a):
        self.x = x
        self.y = y
        self.a = a

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getAngulo(self):
        return self.a

    def equals(self,other):
        return self.x == other.x and self.y == other.y and self.a == other.a