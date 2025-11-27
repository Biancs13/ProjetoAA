import math



class Posicao:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def __eq__(self, other):
        if not isinstance(other, Posicao):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f"({self.x},{self.y})"

def dentroLimites(pos,tamanhoGrelha):
    return 0 <= pos.x < tamanhoGrelha and 0 <= pos.y < tamanhoGrelha

def getDistancia(pos1,pos2):
    return math.hypot(pos1.x-pos2.x,pos1.y-pos2.y)

