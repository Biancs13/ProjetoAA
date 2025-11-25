
from vetor import Vetor, multiplicar_vetor_matriz


class Sensor:
    def __init__(self, campoVisao):
        self.campoVisao = campoVisao

    def getCampoVisao(self):
        return self.campoVisao

#fazer função para rodar os digs
    def rodar(self,novoAngulo):
        novoCampoVisao = []
        for v in self.campoVisao:
            novoCampoVisao.append(rodar(v, novoAngulo))
        self.campoVisao = novoCampoVisao




def rodar(vetor,angulo):
    if angulo == 0:
        return vetor
    elif angulo == 90:
        matriz = [[0, -1], [1, 0]]
    elif angulo == 180:
        matriz = [[-1, 0], [0, -1]]
    else:
        matriz = [[0, 1], [-1, 0]]
    res = multiplicar_vetor_matriz(vetor,matriz)
    return res


print(rodar(Vetor(1,0), 90))  # Saída: [0, 1]
print(rodar(Vetor(1,0), 180)) # Saída: [-1, 0]