import random

import numpy as np

from objetos.acao import Acao


def softmax(x):
    e = np.exp(x - np.max(x))
    return e / np.sum(e)


class RedeNeuronal:

    def __init__(self, tamanho_input, arquitetura_rede, ativacao_rede, output_ativacao, output_dim):
        self.tamanho_input = tamanho_input
        self.arquitetura_rede = arquitetura_rede
        self.ativacao_rede = ativacao_rede
        self.output_ativacao = output_ativacao
        self.NUM_ACOES = 4

    # total de pesos necessários
    def getPesos(self):
        tamanho = self.tamanho_input
        total = 0
        for layer in self.arquitetura_rede:
            total += tamanho * layer + layer
            tamanho = layer

        # output layer (tamanho -> output_dim)
        total += tamanho * self.NUM_ACOES + self.NUM_ACOES
        return total

    def carregaPesos(self, pesos):
        w = np.array(pesos)

        self.pesos_escondidos = []
        self.biases_escondidos = []

        inicio_w = 0
        tamanho = self.tamanho_input

        # camadas escondidas
        for n in self.arquitetura_rede:
            fim_w = inicio_w + (tamanho + 1) * n

            self.biases_escondidos.append(w[inicio_w:inicio_w + n])
            self.pesos_escondidos.append(w[inicio_w + n:fim_w].reshape(tamanho, n))

            inicio_w = fim_w
            tamanho = n

        # camada de output
        self.output_bias = w[inicio_w:inicio_w + self.NUM_ACOES]
        self.output_pesos = w[inicio_w + self.NUM_ACOES:].reshape(tamanho, self.NUM_ACOES)

    # forward pass
    def foward(self, x):
        input = x
        for i in range(len(self.arquitetura_rede)):
            input = getOutput(input, self.pesos_escondidos[i], self.biases_escondidos[i], self.ativacao_rede)

        wx = np.dot(input, self.output_pesos) + self.output_bias
        return self.output_ativacao(wx)

    def decidirAcao(self, estado):
        probabilidades = self.foward(estado)
        index = int(np.argmax(probabilidades))
        return Acao(index)


    # criar rede neuronal com 4 ações (softmax)
def criarRedeNeuronal(tamanho_input):
    fn_camada = lambda x: np.tanh(x)
    fn_output = softmax
    return RedeNeuronal(tamanho_input,(5,5),fn_camada,fn_output,4)


# função auxiliar
def getOutput(inputs, pesos, biases, funcaoAtivacao):
    wx = np.dot(inputs, pesos)
    return funcaoAtivacao(wx + biases)




