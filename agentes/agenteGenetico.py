import random
from agentes.agente import Agente
from objetos.acao import Acao
from objetos.redeNeuronal import criarRedeNeuronal


class AgenteGenetico(Agente):

    def __init__(self, id, posicaoInicial, tipo, angulo, pesos=None):
        super().__init__(id,posicaoInicial,tipo, angulo)
        self.fitness = 0.0
        self.pesos = pesos
        self.rede_neuronal = criarRedeNeuronal(len(self.estadoAtual))
        self.rede_neuronal.carregaPesos(self.pesos)
        self.comportamento = []
        self.pontos_novelty=0.0
#ver pesos

    def age(self):
        acao = self.rede_neuronal.decidirAcao(self.estadoAtual)
        self.comportamento.append(acao)
        return acao

    def avaliacaoEstadoAtual(self,recompensa):
        self.fitness += recompensa

    def reiniciar(self):
        self.fitness = 0
        self.comportamento = []
        self.num_colisoes = 0
        self.num_pontos_recolhidos = 0
        self.condicaoFim = False
        self.behavior = set()
        self.novelty_score = 0.0

    def calcular_fitness_objetivo(self):
        total_pontos = self.num_colisoes * -25
        total_pontos += len(self.comportamento) * 1 - self.num_colisoes
        if self.tipoProblema == "F":
            if self.condicaoFim:
                total_pontos+=500
        elif self.tipoProblema == "R":
            total_pontos += self.num_pontos_recolhidos * 50
        return total_pontos


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