from abc import abstractmethod, ABC

from elemento import Elemento
from observacao import Observacao
from posicao import Posicao, dentroLimites


class Ambiente(ABC):

    def __init__(self,tamanhoGrelha):
        self.grelha = {Posicao(x,y): None for x in range(tamanhoGrelha) for y in range(tamanhoGrelha)}
        self.tamanhoGrelha = tamanhoGrelha

    def observacaoParaAgente(self,agente):
        sensor = agente.getSensor()
        print(" ".join(str(v) for v in sensor.getCampoVisao()))
        observacao = Observacao()
        posicoes = []
        i = 0
        for v in sensor.getCampoVisao(): #Está ordenado esq, frente, dta
            posicao = v.soma(agente.getPosicao())
            if dentroLimites(posicao,self.tamanhoGrelha):
                posicoes.append(posicao)
                observacao.adicionar(self.grelha[posicao].getId() if self.grelha[posicao] is not None else None,i)
                i += 1
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

    #Temos de receber a nova posição do agente para verificar se foi algo coletado, não?
    def atualizacao(self,novaPosAgente = None):
        if novaPosAgente is not None:
            elemento = self.grelha[novaPosAgente]
            if elemento is not None and elemento.isColetavel():
                self.grelha[novaPosAgente] = None


    @abstractmethod
    def condicaoFim(self,agentes=None):
        pass


