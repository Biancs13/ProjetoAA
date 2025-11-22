
from vetor import Vetor, multiplicar_vetor_matriz


class Sensor:
    def __init__(self, campoVisao):
        self.campoVisao = campoVisao

    def getCampoVisao(self):
        return self.campoVisao

    def rodar(self):
        novoCampoVisao = []
        for v in self.campoVisao:
            novoCampoVisao.append(rodar(v))
        self.campoVisao = novoCampoVisao




def rodar(vetor):
    matriz = [[0,-1],[1,0]]
    res = multiplicar_vetor_matriz(vetor,matriz)
    return res

vetor = Vetor(1,1)
print(rodar(vetor))