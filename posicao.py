
class Posicao:
    def __init__(self,x,y,world=None):
        self.x = x
        self.y = y
        self.world = world

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def equals(self,other):
        return self.x == other.x and self.y == other.y