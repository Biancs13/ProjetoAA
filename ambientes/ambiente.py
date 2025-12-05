from abc import abstractmethod, ABC

from objetos.elemento import Elemento
from objetos.observacao import Observacao
from objetos.posicao import Posicao, dentroLimites, getDistancia


class Ambiente(ABC):

    def __init__(self,tamanhoGrelha):
        self.grelha = {Posicao(x,y): Elemento("Vazio",-1,-1,-1) for x in range(tamanhoGrelha) for y in range(tamanhoGrelha)}
        self.tamanhoGrelha = tamanhoGrelha

    def observacaoParaAgente(self,agente):
        sensor = agente.getSensor()
        observacao = Observacao()
        posicoes = []
        i = 0
        for v in sensor.getCampoVisao(): #Está ordenado esq, frente, dta
            posicao = v.soma(agente.getPosicao())
            if dentroLimites(posicao,self.tamanhoGrelha):
                posicoes.append(posicao)
                observacao.adicionar(self.grelha[posicao].getId(),i)
            else:
                observacao.adicionar(None, i)
            i += 1
        return observacao,posicoes


    def agir(self,acao,agente):
        reward = 100
        return reward

    def adicionar(self, elemento, pos):
        if self.grelha[pos].getNome() == "Vazio":
            self.grelha[pos] = elemento
            return True
        else:
            return False

    def getElementos(self,tipo_Elemento):
        elementos = {pos: ele for pos, ele in self.grelha.items() if ele != (-1,-1,-1) and ele.getNome() == tipo_Elemento}
        return elementos

    def getPosicaoElementoMaisProximo(self,posAgente,tipo_elemento):
        elementos = self.getElementos(tipo_elemento)
        if not elementos:      # ← quando não há nenhum elemento desse tipo
            return None
        return min(elementos, key=lambda x: getDistancia(x,posAgente))

    def getElemento(self,pos):
        return self.grelha[pos]

    #Temos de receber a nova posição do agente para verificar se foi algo coletado, não?
    def atualizacao(self,novaPosAgente = None):
        if novaPosAgente != (-1,-1,-1):
            elemento = self.grelha[novaPosAgente]
            if elemento != (-1,-1,-1) and elemento.isColetavel():
                self.grelha[novaPosAgente] = Elemento("Vazio",-1,-1,-1)

    @abstractmethod
    def getRecompensa(self,pos,numColetaveis = 0,pts=0):
        pass

    @abstractmethod
    def condicaoFim(self,agentes=None):
        pass


