import random

from objetos.acao import Acao, melhor_acao_para_direcao
from agentes.agente import Agente
from objetos.vetor import Vetor


class AgenteFixo(Agente):

    def __init__(self, id, posicaoInicial, tipo, angulo):
        super().__init__(id,posicaoInicial,tipo, angulo)
        self.ultima_acao = None

    def age(self):
        print(self.estadoAtual)
        elementos = self.estadoAtual[1:10]
        angulo = self.estadoAtual[0] * 360
        if len(self.estadoAtual) == 12:
            if elementos[2] == 1:
                return Acao.ESQUERDA
            elif elementos[5] == 1:
                return Acao.FRENTE
            elif elementos[8] == 1:
                return Acao.DIREITA
            direcaoFarol = self.estadoAtual[10:]
            vetorFarol = Vetor(direcaoFarol[0], direcaoFarol[1])
            melhorAcao = melhor_acao_para_direcao(angulo, vetorFarol)

            if not existeSolido(elementos, melhorAcao) and not estaFora(elementos,melhorAcao):
                self.ultima_acao = melhorAcao
                return melhorAcao

            alternativas = [Acao.ESQUERDA, Acao.FRENTE, Acao.DIREITA]
            random.shuffle(alternativas)
            alternativas.remove(melhorAcao)
            if self.ultima_acao in alternativas:
                alternativas.remove(self.ultima_acao)

            for acao in alternativas:
                if not existeSolido(elementos, acao) and not estaFora(elementos,acao):
                    self.ultima_acao = acao
                    return acao

            self.ultima_acao = Acao.MEIA_VOLTA
            return Acao.MEIA_VOLTA

        elif len(self.estadoAtual) == 15:
            opcoes = {
                Acao.ESQUERDA: elementos[2],
                Acao.FRENTE:   elementos[5],
                Acao.DIREITA:  elementos[8],
            }
            opcoes_validas = {a: p for a, p in opcoes.items() if p >= 0 and not existeSolido(elementos,a) and not estaFora(elementos,a) } # se existe lá qualquer coletavel
            if opcoes_validas:
                melhor_acao = max(opcoes_validas, key=opcoes_validas.get)
                return melhor_acao
            else:
                numColetaveis = self.estadoAtual[10]
                direcaoNinho = Vetor(self.estadoAtual[11],self.estadoAtual[12])
                direcaoColetavel = Vetor(self.estadoAtual[13],self.estadoAtual[14])
                if self.estadoAtual[13] == -1 and self.estadoAtual[14] == -1:
                    melhorAcao = melhor_acao_para_direcao(angulo, direcaoNinho)
                elif (numColetaveis >= 1):
                    melhorAcao = melhor_acao_para_direcao(angulo, direcaoNinho)
                else:
                    melhorAcao = melhor_acao_para_direcao(angulo, direcaoColetavel)
            print("melhor: ", melhorAcao)
            if melhorAcao == Acao.MEIA_VOLTA:
                return Acao.MEIA_VOLTA
            if not existeSolido(elementos, melhorAcao) and not estaFora(elementos,melhorAcao):
                 return melhorAcao
            outras_acoes = [Acao.ESQUERDA, Acao.FRENTE, Acao.DIREITA]

            outras_acoes.remove(melhorAcao)
            acoes_validas = [a for a in outras_acoes if not existeSolido(elementos, a) and not estaFora(elementos,a)]
            if not acoes_validas:
                 return Acao.MEIA_VOLTA
            escolha = random.choice(acoes_validas)
            return escolha


    def avaliacaoEstadoAtual(self,recompensa):
        pass


def existeSolido(elementos,acao):
    if acao == Acao.ESQUERDA:
        if elementos[1] == 1:
            return True
    elif acao == Acao.FRENTE:
        if elementos[4] == 1:
            return True
    elif acao == Acao.DIREITA:
        if elementos[7] == 1:
            return True
    return False

def estaFora(elementos,acao):
    if acao == Acao.ESQUERDA:
        if elementos[0] == -1 and elementos[1] == 0 and elementos[2] == -1:
            print("entrei")
            return True
    elif acao == Acao.FRENTE:
        if elementos[3] == -1 and elementos[4] == 0 and elementos[5] == -1:
            return True
    elif acao == Acao.DIREITA:
        if elementos[6] == -1 and elementos[7] == 0 and elementos[8] == -1:
            return True
    return False


