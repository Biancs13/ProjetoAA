from controlador import Controlador
from objetos.redeNeuronal import *

class ControladorGenetico(Controlador):

    def __init__(self,geracoes,tamanho_populacao,taxa_mutacao,elite_rate,novelty_weight,k_novel,arquivos_por_geracao,problema,ficheiro_motor,tempo,tipo):
        super().__init__(ficheiro_motor, problema, tempo)
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
        self.tipo = tipo

    def criar_populacao(self):
        return [[random.uniform(-1, 1) for _ in range(self.num_pesos)] for _ in range(self.tamanho_populacao)]

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
        motor = self.criar_motor("genetico")
        agente = motor.agentes[0]
        agente.pesos = pesos
        motor.executa()
        comportamento = tuple(agente.comportamento)
        novelty_total = calcular_novelty(comportamento, self.arquivo, self.k_novel)
        objetivo_total = agente.calcular_fitness_objetivo()
        agente.fitness = objetivo_total + novelty_total * self.novelty_weight
        self.arquivo.add(comportamento)
        return agente,agente.fitness

    def executar(self):
        populacao_pesos = self.criar_populacao()
        for g in range(self.geracoes):
            total_fitness = 0
            fitness_dicionario = {}
            populacao_agentes = []
            i=0
            print(f"\n=== Geração {g+1} ===")
            for ind in populacao_pesos:
                agente,fitness = self.avaliar_individuo(ind)
                fitness_dicionario[tuple(ind)] = fitness
                total_fitness += fitness
                populacao_agentes.append(agente)
                i+=1

            melhor_fitness = max(fitness_dicionario.values())
            fitness_medio = total_fitness / self.tamanho_populacao
            self.fitness_medio_geracao.append(fitness_medio)
            populacao_agentes.sort(key=lambda x: calcular_novelty(x.comportamento, self.arquivo), reverse=True)
            for i in range(self.arquivo_por_geracao):
                self.arquivo.add(tuple(populacao_agentes[i].comportamento))
            populacao_agentes.sort(key=lambda x: x.fitness, reverse=True)
            pesos_ordenados = [agente.pesos for agente in populacao_agentes] #já estão ordenados pelo fitness

            print(f"Gen {g + 1}/{self.geracoes} | Avg Combined: {fitness_medio:.2f} | Melhor fitness: {melhor_fitness:.2f})")

            nova_populacao = []
            n_elite = max(1, int(self.elite_rate * self.tamanho_populacao))
            nova_populacao.extend(pesos_ordenados[:n_elite])
            while len(nova_populacao) < self.tamanho_populacao:
                pai1 = self.selecionar(fitness_dicionario)
                pai2 = self.selecionar(fitness_dicionario)
                filho = self.reproduzir(pai1, pai2)
                self.mutacao(filho, self.taxa_mutacao)
                nova_populacao.append(filho)
            populacao_pesos = nova_populacao


def distancia_jaccard(seq1, seq2):
    s1 = set(seq1)
    s2 = set(seq2)
    intersecao = len(s1 & s2)
    uniao = len(s1 | s2)
    return 0.0 if uniao == 0 else 1.0 - intersecao / uniao

def calcular_novelty(comportamento, arquivo, k=5):
    if not arquivo:
        return 1.0
    distancias = [distancia_jaccard(comportamento, b) for b in arquivo]
    distancias.sort()
    k_use = min(k, len(distancias))
    return sum(distancias[:k_use]) / k_use if k_use > 0 else 0.0


def criaGenetico(ficheiro):
    problema, tempo, politica, tamanhoGeracao, tamanhoPopulacao, taxaMutacao,eliteRate,noveltyWeight,kNovel,arquivosGeracao,ficheiroMotor = ler(ficheiro)
    if verifica([problema, tempo, politica, tamanhoGeracao, tamanhoPopulacao, taxaMutacao, ficheiroMotor]):
        tamanhoGeracao = int(tamanhoGeracao.strip())
        tamanhoPopulacao = int(tamanhoPopulacao.strip())
        taxaMutacao = float(taxaMutacao.strip())
        eliteRate = float(eliteRate.strip())
        noveltyWeight = float(noveltyWeight.strip())
        kNovel = int(kNovel.strip())
        arquivosGeracao = int(arquivosGeracao.strip())
        controlador = ControladorGenetico(tamanhoGeracao,tamanhoPopulacao,taxaMutacao,eliteRate,noveltyWeight,kNovel,arquivosGeracao,problema,ficheiroMotor,tempo,problema)
        return controlador


#não atualizado para o novo ficheiro
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
    if taxaMut <= 0 or taxaMut > 1 or type(taxaMut) is not float:
        return False
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
    eliteRate = linhas[i].strip()
    i += 1
    noveltyWeight = linhas[i].strip()
    i += 1
    kNovel = linhas[i].strip()
    i += 1
    arquivosGeracao = linhas[i].strip()
    i += 1
    partes = linhas[i].split()
    if partes[0] == "MS":
        fichMotor = "./" + partes[1]
    else:
        fichMotor = None
    resultado = [tipo,tempo,politica,tamanhoGer,tamanhoPop,taxaMut,eliteRate,noveltyWeight,kNovel,arquivosGeracao,fichMotor]
    return resultado


controlador = criaGenetico("controladorGenetico_farol.txt")
if controlador:
    controlador.executar()
