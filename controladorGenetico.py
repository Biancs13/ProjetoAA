import random
from motorSimulacao import MotorSimulacao, cria
from objetos.redeNeuronal import *

class ControladorGenetico:

    def _init_(self,geracoes, tamanho_populacao, taxa_mutacao,problema, ficheiro):
        self.geracoes = geracoes
        self.tamanho_populacao = tamanho_populacao
        self.taxa_mutacao = taxa_mutacao
        if problema == "F":
            self.tamanho_individuo = 12
        else:
            self.tamanho_individuo = 15
        self.ficheiro = ficheiro
        self.elite_rate = 0.1
        self.novelty_weight = 1000
        self.k_novel = 5
        self.arquivo_por_geracao = 5
        self.arquivo = set()
        self.fitness_medio_geracao = []

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

    def avaliar_individuo(self, pesos):
        motor = cria(self.ficheiro)
        for ag in motor.agentes:
            ag.pesos=pesos
            ag.reiniciar()
        motor.execute()
        fitness_total = 0
        for ag in motor.agentes:
            comportamento = set(ag.comportamento)
            novelty_total = calcular_novelty(comportamento, self.arquivo, k=self.k_novel)
            objetivo_total = ag.calcular_fitness_objetivo()
            ag.fitness = objetivo_total + novelty_total * self.novelty_weight
            fitness_total += ag.fitness
            self.arquivo.add(comportamento)
        return fitness_total / len(motor.agentes)

    def executar(self):
        populacao_pesos = self.criar_populacao()
        populacao_agentes = []


        for g in range(self.geracoes):
            total_fitness = 0
            fitness_dicionario = {}
            print(f"\n=== Geração {g} ===")
            for ind in populacao_pesos:
                fitness = self.avaliar_individuo(ind)
                fitness_dicionario[ind] = fitness
                total_fitness += fitness

            populacao_agentes.sort(key=lambda x: x.fitness, reverse=True)
            fitness_medio = total_fitness / self.tamanho_populacao
            self.fitness_medio_geracao.append(fitness_medio)
            melhor_novelty = calcular_novelty(populacao_agentes[0], self.arquivo)
            melhor_objetivo = populacao_agentes[0].calcular_fitness_objetivo()

            print(f"Gen {g + 1}/{self.geracoes} | Avg Combined: {fitness_medio:.2f} | Best Combined: {populacao_agentes[0].combined_fitness:.2f} (Nov: {melhor_novelty:.2f}, Obj: {melhor_objetivo:.2f})")

            populacao_agentes.sort(key=lambda x: calcular_novelty(x.comportamento, self.arquivo), reverse=True)

            for i in range(self.arquivo_por_geracao):
                self.arquivo.add(populacao_agentes[i].comportamento)

            populacao_agentes.sort(key=lambda x: x.fitness, reverse=True)
            pesos_ordenados = [agente.pesos for agente in populacao_agentes]

            nova_populacao = []

            n_elite = self.elite_rate*self.tamanho_populacao
            nova_populacao.extend(pesos_ordenados[:n_elite])

            while len(nova_populacao) < self.tamanho_populacao:
                pai1 = self.selecionar(fitness_dicionario)
                pai2 = self.selecionar(fitness_dicionario)
                filho = self.reproduzir(pai1, pai2)
                self.mutacao(filho, self.taxa_mutacao)
                nova_populacao.append(filho)

            populacao_pesos = nova_populacao


def distancia_jaccard(set1, set2):
    intersecao = len(set1 & set2)
    uniao = len(set1 | set2)
    return 1 - intersecao / uniao if uniao != 0 else 0

def calcular_novelty(comportamento, arquivo, k=5):
    if not arquivo:
        return 1.0
    distancias = [distancia_jaccard(comportamento, b) for b in arquivo]
    distancias.sort()
    return sum(distancias[:k]) / k if len(distancias) >= k else sum(distancias) / len(distancias)


def criaGenetico(ficheiro):
    problema, tempo, politica, tamanhoGeracao, tamanhoPopulacao, taxaMutacao, ficheiroMotor = ler(ficheiro)
    print(verifica([problema, tempo, politica, tamanhoGeracao, tamanhoPopulacao, taxaMutacao, ficheiroMotor]))
    if verifica([problema, tempo, politica, tamanhoGeracao, tamanhoPopulacao, taxaMutacao, ficheiroMotor]):
        tamanhoGeracao = int(tamanhoGeracao.strip())
        tamanhoPopulacao = int(tamanhoPopulacao.strip())
        taxaMutacao = float(taxaMutacao.strip())
        ms = cria(ficheiroMotor,problema,tempo,politica)
        controlador = ControladorGenetico(tamanhoGeracao,tamanhoPopulacao,taxaMutacao,problema,ms)
        return controlador



def verifica(resultado):
    ambiente, tempo, politica, tamanhoGer, tamanhoPop, taxaMut, fichMotor = resultado
    if ambiente not in ["R","F"]:
        return False

    if ambiente == "R":
        limite = int(tempo)
        if limite <= 10 or type(limite) is not int:
            return False

    if politica not in ["fixo","aleatorio","reforco","genetico"]:
        return False

    tamanhoGeracao = int(tamanhoGer)
    if tamanhoGeracao <= 10 or type(tamanhoGeracao) is not int:
        return False

    tamanhoPopulacao = int(tamanhoPop)
    if tamanhoPopulacao <= 10 or type(tamanhoPopulacao) is not int:
        return False

    taxaMut = float(taxaMut)
    if taxaMut <= 0 or type(taxaMut) is not float:
        return False

    #python é estúpido
    #if not os.path.exists(fichMotor) or not os.path.isfile(fichMotor):
    #    return False

    return True

def ler(nome):
    fich = open(nome, "r")
    linhas = fich.readlines()
    fich.close()
    tipo = linhas[0].strip()
    i=1
    if tipo == "R":
        tempo = linhas[i].strip()
        i+=1
    else:
        tempo = None

    politica = linhas[i].strip()
    i+=1

    tamanhoGer = linhas[i].strip()
    i+=1

    tamanhoPop = linhas[i].strip()
    i+=1

    taxaMut = linhas[i].strip()
    i+=1

    partes = linhas[i].split()
    if partes[0] == "MS":
        fichMotor = "./" + partes[1]
    else:
        fichMotor = None

    resultado = [tipo,tempo,politica,tamanhoGer,tamanhoPop,taxaMut,fichMotor]

    return resultado

