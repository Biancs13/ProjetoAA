from abc import abstractmethod

from elemento import Elemento
from observacao import Observacao
from posicao import Posicao, dentroLimites


class Ambiente:

    def __init__(self,tamanhoGrelha):
        self.grelha = {Posicao(x,y): None for x in range(tamanhoGrelha) for y in range(tamanhoGrelha)}
        self.tamanhoGrelha = tamanhoGrelha

    def observacaoParaAgente(self,agente):
        sensor = agente.getSensor()
        print(" ".join(str(v) for v in sensor.getCampoVisao()))
        observacao = Observacao()
        posicoes = []
        for v in sensor.getCampoVisao():
            posicao = v.soma(agente.getPosicao())
            if dentroLimites(posicao,self.tamanhoGrelha):
                posicoes.append(posicao)
                observacao.adicionar(v,self.grelha[posicao].getId() if self.grelha[posicao] is not None else None)
        return observacao,posicoes


    def agir(self,acao,agente):
        reward = 100
        return reward

    def adicionar(self,elemento,pos):
        if self.grelha[pos] is None:
            self.grelha[pos] = elemento
            return True
        else:
            return False

    def getElementos(self,tipo_Elemento):
        elementos = {pos: ele for pos, ele in self.grelha.items() if ele is not None and ele.getNome() == tipo_Elemento}
        return elementos

    def getElemento(self,pos):
        return self.grelha[pos]

    def atualizacao(self):
        pass

    @abstractmethod
    def condicaoFim(self,agentes=None):
        pass

ambiente = Ambiente(20)
elemento = Elemento("parede", -10, False, True)
print(ambiente.grelha)
ambiente.adicionar(elemento,Posicao(1,1))
print(ambiente)

