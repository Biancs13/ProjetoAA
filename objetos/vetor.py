import math

from objetos.posicao import Posicao

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


def getDirecao(pos1, pos2):
    dx = pos2.x - pos1.x
    dy = pos2.y - pos1.y
    norm = math.sqrt(dx*dx + dy*dy)
    if norm == 0:
        return Vetor(0, 0)
    return Vetor(dx / norm, dy / norm)

def multiplicar_vetor_matriz(vetor, matriz):
    x = vetor.x * matriz[0][0] + vetor.y * matriz[0][1]
    y = vetor.x * matriz[1][0] + vetor.y * matriz[1][1]
    return Vetor(x,y)


def vetor_para_angulo(vetor):
    ang_std = math.degrees(math.atan2(vetor.y, vetor.x)) % 360
    return ang_std

def angulo_normalizado(v1, v2):
    #cálculo da norma do vetor
    n1 = math.hypot(v1.x, v1.y)
    n2 = math.hypot(v2.x, v2.y)

    if n1 == 0 or n2 == 0:
        return 0.0

    dot = v1.x * v2.x + v1.y * v2.y
    cross = v1.x * v2.y - v1.y * v2.x  # z do produto vetorial 2D

    angulo = math.atan2(cross, dot)
    return angulo / math.pi

