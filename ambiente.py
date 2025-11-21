from elemento import Elemento
from observacao import Observacao
from posicao import Posicao


class Ambiente:

    def __init__(self,tamanhoGrelha):
        self.grelha = {Posicao(x,y):None for x in range(tamanhoGrelha) for y in range(tamanhoGrelha)}
        self.tamanhoGrelha = tamanhoGrelha

    def observacaoParaAgente(self,agente):
        sensor = agente.getSensor()
        observacao = Observacao()
        for v in sensor.getCampoVisao():
            posicao = v.soma(agente.getPosicao())
            observacao.adicionar(v,self.grelha[posicao].getId())

    def agir(self,acao,agente):
        reward = 100
        return reward



    def adicionar(self,elemento,pos):
        if self.grelha[pos] is None:
            self.grelha[pos] = elemento
            return True
        else:
            return False





ambiente = Ambiente(20)
elemento = Elemento("parede", -10, False, True)
print(ambiente.grelha)
ambiente.adicionar(elemento,Posicao(1,1))
print(ambiente)

