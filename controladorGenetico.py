import random
from objetos.redeNeuronal import *

class ControladorGenetico:

    def __init__(self,geracoes, tamanho_populacao, taxa_mutacao,problema, motorSimulacao):
        self.geracoes = geracoes
        self.tamanho_populacao = tamanho_populacao
        self.taxa_mutacao = taxa_mutacao
        if problema == "F":
            estado_tamanho = 12
        else:
            estado_tamanho = 15
        self.tamanho_individuo = estado_tamanho
        self.elite_rate = 0.1
        self.novelty_weight = 1000
        self.k_novel = 5
        self.arquivo_por_geracao = 5
        #self.procura_novelty = NoveltySearch(self.k_novel,self.arquivo_por_geracao)
        self.archive = []
        self.motor = motorSimulacao


    def criar_populacao(self):
        return [[random.uniform(-1, 1) for _ in range(self.tamanho_individuo)] for _ in range(self.tamanho_populacao)]

    def selecionar(self,fitness_dict,tamanho_torneio=2):
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

'''
def fitness(individuo, funcao_fitness, n=5):
    total = 0
    for _ in range(n):
        total += funcao_fitness(individuo, random.randint(1,100))
    return total // n
'''

def executar(self):
    populacao = self.criar_populacao()
    fitness_dict = {}

    for g in range(self.geracoes):
        total_fitness = 0
        print(f"\n=== Geração {g} ===")
        for ind in populacao:
            self.motor.executa()
            key = tuple(ind)
            if key not in fitness_dict:
                fitness_dict[key] = self.avaliar_individuo(ind)

        fitnesses = list(fitness_dict.values())
        best = max(fitnesses)
        media = sum(fitnesses) / len(fitnesses)
        dp = np.std(fitnesses)

        print(f"Melhor fitness: {best}")
        print(f"Média da população: {media:.2f}")

        if best >= self.target_fitness:
            break

        escala = 0.3 if dp < 7.5 else 0.1

        elites = sorted(
            populacao,
            key=lambda ind: fitness_dict[tuple(ind)],
            reverse=True
        )[: int(self.elite_rate * self.tamanho_populacao)]

        nova_pop = elites[:]

        while len(nova_pop) < self.tamanho_populacao:
            pai1 = self.selecionar(fitness_dict)
            pai2 = self.selecionar(fitness_dict)
            filho = self.reproduzir(pai1, pai2)
            self.mutacao(filho, escala)
            nova_pop.append(filho)

        populacao = nova_pop
        elite_keys = [tuple(e) for e in elites]
        fitness_dict = {k: v for k, v in fitness_dict.items() if k in elite_keys}

    melhor = max(fitness_dict, key=fitness_dict.get)
    return list(melhor), fitness_dict[melhor]

def jaccard_distance(set1, set2):
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return 1 - intersection / union if union != 0 else 0

def compute_novelty(current_behavior, archive, k=5):
    #empty archive case
    if not archive:
        # The first item is, by definition, maximally novel
        return 1.0

    distances = [jaccard_distance(current_behavior, b) for b in archive]
    distances.sort()
    return sum(distances[:k]) / k if len(distances) >= k else sum(distances) / len(distances)




