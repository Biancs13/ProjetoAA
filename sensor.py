import numpy as np

class Sensor:
    def __init__(self, campoVisao):
        self.campoVisao = campoVisao

    def getCampoVisao(self):
        return self.campoVisao

    def rodar(self,numVezes=1):
        novoSensor = []
        for v in self.campoVisao:
            for i in range(numVezes):
                novoSensor.append(rodar(v))
        return novoSensor



def rodar(vetor):
    matriz = np.array([[0,1],[-1,0]])
    res = np.array(vetor) @ matriz
    return tuple(int(x) for x in res)

vetor = (0,1)
print(rodar(vetor))