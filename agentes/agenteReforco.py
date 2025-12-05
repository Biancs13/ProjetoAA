from abc import ABC

from agentes.agente import Agente
from objetos.acao import Acao


class AgenteReforco(Agente):

    def __init__(self, id, posicaoInicial, tipo, angulo):
        super().__init__(id,posicaoInicial,tipo, angulo)
        self.posiccoesBloqueadas = []
        self.ultimaPosicao = posicaoInicial

    def age(self):
        pass

    def avaliacaoEstadoAtual(self,recompensa):
        pass

def escreverDicionario(dic,nome):
    dados = []
    for estado, acaoRecompensa in dic.items():
        for acao,recompensa in acaoRecompensa.items():
            linha = f"{'|'.join(map(str, estado))},{acao.name},{str(recompensa)}"
            dados.append(linha)
    ficheiro = open(nome,'w')
    for linha in dados:
        ficheiro.write(linha + '\n')

def lerDicionario(nome):
    dic = {}
    ficheiro = open(nome,'r')
    for linha in ficheiro:
        linha = linha.strip()
        if not linha:
            continue
        partes = linha.split(',')
        if len(partes) == 3:
            estado_str = partes[0]
            acao_str = partes[1]
            recompensa = int(partes[2])

            estado = [int(e) for e in estado_str.split('|')]
            chave = tuple(estado)
            acao = Acao[acao_str]

            if chave not in dic:
                dic[chave] = {}
            dic[chave][acao] = recompensa

    return dic

if __name__ == '__main__':
    NOME_FICHEIRO = "teste.txt"
    q_table_original = {
        (0, -1, 0, -1, 0, 0, 1): {
            Acao.FRENTE: 10,
            Acao.DIREITA: -5
        },
        (0, 0, 0, 0, -1, -1): {
            Acao.ESQUERDA: 5,
            Acao.MEIA_VOLTA: 0
        }
    }

    print("--- Início do Teste ---")
    print(f"Original: {q_table_original}")
    escreverDicionario(q_table_original, NOME_FICHEIRO)
    q_table_carregada = lerDicionario(NOME_FICHEIRO)

    print(f"\nCarregada: {q_table_carregada}")