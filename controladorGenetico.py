from controlador import Controlador
from objetos.acao import atuar
from objetos.posicao import Posicao
from objetos.redeNeuronal import *

class ControladorGenetico(Controlador):

    def __init__(self,geracoes,tamanho_populacao,taxa_mutacao,elite_rate,novelty_weight,k_novel,arquivos_por_geracao,problema,ficheiro_motor,tempo,modo,tamanho_torneio):
        super().__init__(ficheiro_motor, problema, tempo,modo)
        self.geracoes = geracoes
        self.tamanho_populacao = tamanho_populacao
        self.taxa_mutacao = taxa_mutacao
        self.num_pesos = 44 if problema == "F" else 50
        self.elite_rate = elite_rate
        self.novelty_weight = novelty_weight
        self.k_novel = k_novel
        self.arquivos_por_geracao = arquivos_por_geracao
        self.arquivo = set()
        self.fitness_medio_geracao = []
        self.numero_passos = []
        self.modo = modo
        self.tamanho_torneio = tamanho_torneio
        self.melhores_caminhos_gen = []

    def criar_populacao(self):
        return [[random.uniform(-1, 1) for _ in range(self.num_pesos)] for _ in range(self.tamanho_populacao)]

    def selecionar(self,fitness_dict,tamanho_torneio):
        torneio = random.sample(list(fitness_dict.items()), tamanho_torneio)
        return max(torneio, key=lambda x: x[1])[0]

    def reproduzir(self, pai1, pai2):
        alpha = random.uniform(0, 1)
        return [alpha * a + (1 - alpha) * b for a, b in zip(pai1, pai2)]

    def mutacao(self,individuo, escala):
        for i in range(len(individuo)):
            if random.random() < self.taxa_mutacao:
                individuo[i] += random.gauss(0, escala)
                individuo[i] = max(-1, min(1, individuo[i]))

    def avaliar_individuo(self, pesos):
        motor = self.criar_motor("genetico")
        ambiente = motor.ambiente
        agente = motor.agentes[0]
        agente.pesos = pesos
        motor.executa()
        comportamento = tuple(agente.comportamento)
        objetivo_total = agente.calcular_fitness_objetivo(ambiente)
        novelty_total = calcular_novelty(comportamento, self.arquivo, self.k_novel)
        agente.fitness = objetivo_total + novelty_total * self.novelty_weight
        self.arquivo.add(comportamento)
        return agente,agente.fitness

    def executar_aprendizagem(self):
        populacao_pesos = self.criar_populacao()
        melhor_agente,melhor_fitness_global = None, -float('inf')
        for g in range(self.geracoes):
            total_fitness = 0
            fitness_dicionario = {}
            populacao_agentes = []
            i=0
            for ind in populacao_pesos:
                agente,fitness = self.avaliar_individuo(ind)
                fitness_dicionario[tuple(ind)] = fitness
                total_fitness += fitness
                populacao_agentes.append(agente)
                i+=1
            melhor_fitness = max(fitness_dicionario.values())
            fitness_medio = total_fitness / self.tamanho_populacao
            self.fitness_medio_geracao.append(fitness_medio)
            agente_melhor_geracao = max(populacao_agentes, key=lambda x: x.fitness)
            if melhor_fitness > melhor_fitness_global:
                melhor_fitness_global = melhor_fitness
                melhor_agente = agente_melhor_geracao
            self.melhores_caminhos_gen.append(melhor_agente.comportamento)
            self.numero_passos.append(melhor_agente.num_passos)
            populacao_agentes.sort(key=lambda x: calcular_novelty(x.comportamento, self.arquivo,self.k_novel), reverse=True)
            for i in range(self.arquivos_por_geracao):
                self.arquivo.add(tuple(populacao_agentes[i].comportamento))
            populacao_agentes.sort(key=lambda x: x.fitness, reverse=True)
            pesos_ordenados = [agente.pesos for agente in populacao_agentes] #já ordenados pelo fitness

            print(f"Gen {g + 1}/{self.geracoes} | Avg Combined: {fitness_medio:.2f} | Melhor fitness: {melhor_fitness:.2f})")

            nova_populacao = []
            n_elite = max(1, int(self.elite_rate * self.tamanho_populacao))
            nova_populacao.extend(pesos_ordenados[:n_elite])
            while len(nova_populacao) < self.tamanho_populacao:
                pai1 = self.selecionar(fitness_dicionario,self.tamanho_torneio)
                pai2 = self.selecionar(fitness_dicionario,self.tamanho_torneio)
                filho = self.reproduzir(pai1, pai2)
                self.mutacao(filho, self.taxa_mutacao)
                nova_populacao.append(filho)
            populacao_pesos = nova_populacao
        if melhor_agente is not None:
            melhor_agente.escreverMelhor()

    def executar_teste(self):
        motor = self.criar_motor("genetico")
        motor.executa()


def distancia_jaccard(seq1, seq2):
    s1 = set(seq1)
    s2 = set(seq2)
    intersecao = len(s1 & s2)
    uniao = len(s1 | s2)
    return 0.0 if uniao == 0 else 1.0 - intersecao / uniao

def calcular_novelty(comportamento, arquivo, k):
    if not arquivo:
        return 1.0
    distancias = [distancia_jaccard(comportamento, b) for b in arquivo]
    distancias.sort()
    k_use = min(k, len(distancias))
    return sum(distancias[:k_use]) / k_use if k_use > 0 else 0.0




#Para os gráficos
def reconstruir_caminho(posicao,angulo, comportamento):
    caminho = [posicao]
    for a in comportamento:
        posicao, angulo = atuar(posicao,angulo,a)
        caminho.append(posicao)
    return caminho

#Assumimos que os caminhos já estão calculados
def calcular_mapa(caminhos,tamanho_grelha):
    mapa_visitas = {Posicao(x,y):0 for x in range(tamanho_grelha) for y in range(tamanho_grelha)}
    for c in caminhos:
        for pos in c:
            mapa_visitas[pos] = mapa_visitas[pos] + 1
    return mapa_visitas



# TODO Acrescentar verifica ao conteudo APENAS !!!
def criaGenetico(modo,problema,conteudo):
    tamanho_geracao, tamanho_populacao, taxa_mutacao,elite_rate,novelty_weight,k_novel,arquivos_geracao,torneio,ficheiro_motor = conteudo
    tamanho_geracao = int(tamanho_geracao.strip())
    tamanho_populacao = int(tamanho_populacao.strip())
    taxa_mutacao = float(taxa_mutacao.strip())
    elite_rate = float(elite_rate.strip())
    novelty_weight = float(novelty_weight.strip())
    k_novel = int(k_novel.strip())
    arquivos_geracao = int(arquivos_geracao.strip())
    torneio = int(torneio.strip())
    problema = problema.split(" ")
    if problema[0] == "R":
        tempo = int(problema[1])
    else:
        tempo = None
    ficheiro_motor = ficheiro_motor.split(" ")[1]
    controlador = ControladorGenetico(tamanho_geracao,tamanho_populacao,taxa_mutacao,elite_rate,novelty_weight,k_novel,arquivos_geracao,problema[0],ficheiro_motor,tempo,modo,torneio)
    return controlador

