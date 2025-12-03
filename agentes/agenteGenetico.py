import random
from agentes.agente import Agente
from objetos.acao import Acao
from objetos.redeNeuronal import criarRedeNeuronal


class AgenteGenetico(Agente):

    def __init__(self, id, posicaoInicial, tipo, angulo, pesos,redeNeuronal):
        super().__init__(id,posicaoInicial,tipo, angulo)
        self.fitness = 0.0
        self.pesos = pesos
        self.rede_neuronal = criarRedeNeuronal(len(self.estadoAtual))
        self.rede_neuronal.carregaPesos(self.pesos)
        self.comportamento = []
        self.pontos_novelty=0.0

    def age(self):
        acoes = list(Acao)





        for v in self.estadoAtual:
            estado.append(0.0 if v is None else float(v))
        n = len(estado)
        pontos = []
        for i in range(4):
            inicio = i * n
            fim = inicio + n
            w = self.pesos[inicio:fim]
            ponto = sum(e*p for e,p in zip(estado,w))
            pontos.append(ponto)
        #ver caso empate
        return acoes[pontos.index(max(pontos))]

    def avaliacaoEstadoAtual(self,recompensa):
        self.fitness += recompensa

    def reiniciar(self):
        self.fitness = 0
        self.behavior = set()
        self.novelty_score = 0.0

def escreverPesos(ficheiro,lista):
    fich = open(ficheiro,'w')
    for i in lista:
        fich.write(str(i) + '\n')

def lerPesos(ficheiro,tamanhoLista):
    fich = open(ficheiro,'r')
    lista = [linha.strip() for linha in fich.readlines()]
    correto = valida(lista,tamanhoLista)
    resultado = []
    if correto:
        for i in lista:
            resultado.append(float(i))
        return resultado
    return None


def valida(lista,tamanhoLista):
    for i in lista:
        if float(i) is not float:
            return False
    if tamanhoLista == len(lista):
        return False
    return True

if __name__ == "__main__":
    nome_ficheiro = "teste_pesos.txt"
    tamanho_esperado = 20
    pesos_originais = [round(random.uniform(-1, 1), 6) for _ in range(tamanho_esperado)]
    escreverPesos(nome_ficheiro, pesos_originais)
    pesos_lidos = lerPesos(nome_ficheiro, tamanho_esperado)
    for p in pesos_lidos:
        print(p)
    nome_ficheiro2 = "teste_errado.txt"
    escreverPesos(nome_ficheiro2, [0.5, "ERRO_STRING", 0.9])
    pesos_lidos_falha_tipo = lerPesos(nome_ficheiro2, 3)
    print(pesos_lidos_falha_tipo)