import random
from abc import ABC

from agentes.agente import Agente
from objetos.acao import getAcaoAleatoria, Acao

from objetos.acao import Acao


class AgenteReforco(Agente):

    def __init__(self, id, posicaoInicial, tipo, angulo, ficheiro, alpha, desconto, epsilon_inicial, epsilon_final,num_episodios):
        super().__init__(id,posicaoInicial,tipo, angulo,ficheiro)
        self.q = {} # Dicionario de dicionarios, para cada estado damos um dicionario com acao,Q
        self.alpha = alpha
        self.desconto = desconto
        self.num_episodios = num_episodios
        self.epsilon_inicial = epsilon_inicial
        self.epsilon = epsilon_inicial
        self.epsilon_final = epsilon_final
        self.ultima_acao = None

    def age(self):
        self.ultima_acao = self.escolher_acao()
        self.num_passos += 1
        return self.ultima_acao

    #Para que o Q learning nao crie imensas linhas
    def _obter_chave_estado(self, estado_original):
        return tuple(round(e, 2) for e in estado_original)

    def escolher_acao(self):
        if random.random() < self.epsilon:
            return getAcaoAleatoria()
        else:
            return self.getAcaoComMaiorQ()

    def getAcaoComMaiorQ(self):
        estado = self._obter_chave_estado(self.estadoAntigo)
        if estado not in self.q:
            self.q[estado] = {acao: 0 for acao in list(Acao)}
            return getAcaoAleatoria()

        dic_acoes = self.q[estado]
        max_q = max(dic_acoes.values())
        melhores_acoes = [acao for acao, q in dic_acoes.items() if q == max_q]
        return random.choice(melhores_acoes) # para lidar com empates


    #na verdade aqui é avaliacao do EstadoAntigo  Podemos mudar
    def avaliacaoEstadoAtual(self,recompensa):
        if self.ultima_acao is None or self.estadoAntigo is None:
            return
        estado_atual = self._obter_chave_estado(self.estadoAtual)
        estado_antigo = self._obter_chave_estado(self.estadoAntigo)

        if estado_antigo not in self.q:
            self.q[estado_antigo] = {acao: 0 for acao in list(Acao)}

        q_atual = self.q[estado_antigo][self.ultima_acao]

        if estado_atual not in self.q:
            self.q[estado_atual] = {acao: 0 for acao in list(Acao)}

        max_q_novo = max(self.q[estado_atual].values(), default=0)

        self.q[estado_antigo][self.ultima_acao] =(
                q_atual + self.alpha * (recompensa + self.desconto*max_q_novo - q_atual))

    def atualizar_epsilon(self, episodio):
        ratio = episodio / self.num_episodios
        self.epsilon = max(
            self.epsilon_final,
            self.epsilon_inicial * (1 - ratio)
        )

    def escreverMelhor(self):
        dados = []
        for estado, acaoRecompensa in self.q.items():
            for acao,recompensa in acaoRecompensa.items():
                linha = f"{'|'.join(f'{e:.2f}' for e in estado)},{acao.name},{recompensa:.2f}"
                dados.append(linha)
        fich = open(self.ficheiro,'r+')
        linhas = fich.readlines()
        primeiras = linhas[:8]
        fich.seek(0)
        for linha in primeiras:
            fich.write(linha)
        for linha in dados:
            fich.write('\n' + linha)

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
            recompensa = float(partes[2])
            estado = [float(e) for e in estado_str.split('|')]
            chave = tuple(estado)
            acao = Acao[acao_str]
            if chave not in dic:
                dic[chave] = {}
            dic[chave][acao] = recompensa
    return dic