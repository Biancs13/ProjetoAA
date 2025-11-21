from posicao import Posicao

class Vetor:
    def __init__(self, x,y):
        self.x = x
        self.y = y

    def soma(self,pos):
        x = pos.getX() + self.x
        y = pos.getY() + self.y
        return Posicao(x,y)

    def __eq__(self, other):
        return isinstance(other, Vetor) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f'v({self.x},{self.y})'

def multiplicar_vetor_matriz(vetor, matriz):
    x = vetor.x * matriz[0][0] + vetor.y * matriz[0][1]
    y = vetor.x * matriz[1][0] + vetor.y * matriz[1][1]
    return Vetor(x,y)
