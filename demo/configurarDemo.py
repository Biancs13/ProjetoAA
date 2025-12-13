from controlador import *

paredes = \
"""E parede (4,3) False True 0
E parede (4,4) False True 0
E parede (4,5) False True 0
E parede (4,6) False True 0
E parede (4,7) False True 0
E parede (2,18) False True 0
E parede (3,18) False True 0
E parede (4,18) False True 0
E parede (5,8) False True 0
E parede (5,9) False True 0
E parede (5,10) False True 0
E parede (5,13) False True 0
E parede (5,14) False True 0
E parede (5,15) False True 0
E parede (5,16) False True 0
E parede (5,18) False True 0
E parede (6,18) False True 0
E parede (7,18) False True 0
E parede (8,18) False True 0
E parede (8,10) False True 0
E parede (9,10) False True 0
E parede (9,18) False True 0
E parede (10,10) False True 0
E parede (10,18) False True 0
E parede (11,10) False True 0
E parede (11,18) False True 0
E parede (12,10) False True 0
E parede (12,18) False True 0
E parede (13,10) False True 0
E parede (14,0) False True 0
E parede (14,1) False True 0
E parede (14,2) False True 0
E parede (14,3) False True 0
E parede (14,4) False True 0
E parede (14,5) False True 0
E parede (14,6) False True 0
E parede (14,10) False True 0
E parede (15,10) False True 0
E parede (16,10) False True 0"""


coletaveis_e_ninhos = """E ovo (2,3) True False 6
E ovo (3,17) True False 6
E ovo (5,7) True False 7
E ovo (7,8) True False 5
E ovo (10,4) True False 6
E ovo (12,16) True False 7
E ovo (15,6) True False 5
E ovo (17,11) True False 6
E ninho (4,9) False False 0
E ninho (15,3) False False 0
E ninho (18,18) False False 0"""



ambiente_farol_sem_paredes = f"""E farol (18,18) False False 100"""

ambiente_farol_com_paredes = f"""E farol (18,18) False False 100
{paredes}
"""

ambiente_recolecao_sem_paredes = coletaveis_e_ninhos

ambiente_recolecao_com_paredes = coletaveis_e_ninhos + "\n" + paredes


#Fixo e Aleatório
def resetFarol(ficheiro_controlador, ficheiro_simulacao, ficheiro_agente,politica,ambiente):
    texto_controlador = f"A\nF\n{politica}\nMS {ficheiro_simulacao}"
    texto_simulacao = f"20\n150\nAG {ficheiro_agente}\n{ambiente}"
    texto_agente = "1\n(0,0)\n0\nS (0,-1) (0,1) (1,0)"

    with open(ficheiro_controlador, "w", encoding="utf-8") as f:
        f.write(texto_controlador)
    with open(ficheiro_simulacao, "w", encoding="utf-8") as f:
        f.write(texto_simulacao)
    with open("../agentes/" + ficheiro_agente, "w", encoding="utf-8") as f:
        f.write(texto_agente)


def resetRecolecao(ficheiro_controlador, ficheiro_simulacao, ficheiro_agente,politica,ambiente,tempo):
    texto_controlador = f"A\nR {tempo}\n{politica}\nMS {ficheiro_simulacao}"
    texto_simulacao = f"20\n150\nAG {ficheiro_agente}\n{ambiente}"
    texto_agente = "1\n(0,0)\n0\nS (0,-1) (0,1) (1,0)"

    with open(ficheiro_controlador, "w", encoding="utf-8") as f:
        f.write(texto_controlador)
    with open(ficheiro_simulacao, "w", encoding="utf-8") as f:
        f.write(texto_simulacao)
    with open("../agentes/" + ficheiro_agente, "w", encoding="utf-8") as f:
        f.write(texto_agente)

#Genetico
def resetFarolGenetico(ficheiro_controlador, ficheiro_simulacao, ficheiro_agente, ambiente, politica,geracoes,num_individuos,taxa_mutacao,taxa_elite,novelty_weight,num_novelty,num_archives,torneio):
    texto_controlador = f"A\nF\n{politica}\n{geracoes}\n{num_individuos}\n{taxa_mutacao}\n{taxa_elite}\n{novelty_weight}\n{num_novelty}\n{num_archives}\n{torneio}\nMS {ficheiro_simulacao}"
    texto_simulacao = f"20\n150\nAG {ficheiro_agente}\n{ambiente}"
    texto_agente = "1\n(0,0)\n0\nS (0,-1) (0,1) (1,0)"

    with open(ficheiro_controlador, "w", encoding="utf-8") as f:
        f.write(texto_controlador)
    with open(ficheiro_simulacao, "w", encoding="utf-8") as f:
        f.write(texto_simulacao)
    with open("../agentes/" + ficheiro_agente, "w", encoding="utf-8") as f:
        f.write(texto_agente)

def resetRecolecaoGenetico(ficheiro_controlador, ficheiro_simulacao, ficheiro_agente, politica, ambiente, tempo,geracoes,num_individuos,taxa_mutacao,taxa_elite,novelty_weight,num_novelty,num_archives,torneio):
    texto_controlador = f"A\nR {tempo}\n{politica}\n{geracoes}\n{num_individuos}\n{taxa_mutacao}\n{taxa_elite}\n{novelty_weight}\n{num_novelty}\n{num_archives}\n{torneio}\nMS {ficheiro_simulacao}"
    texto_simulacao = f"20\n150\nAG {ficheiro_agente}\n{ambiente}"
    texto_agente = "1\n(0,0)\n0\nS (0,-1) (0,1) (1,0)"

    with open(ficheiro_controlador, "w", encoding="utf-8") as f:
        f.write(texto_controlador)
    with open(ficheiro_simulacao, "w", encoding="utf-8") as f:
        f.write(texto_simulacao)
    with open("../agentes/" + ficheiro_agente, "w", encoding="utf-8") as f:
        f.write(texto_agente)


#Reforco
def resetFarolReforco(ficheiro_controlador, ficheiro_simulacao, ficheiro_agente, politica,ambiente,episodios,alpha,gama,eps_inicial,eps_final):
    texto_controlador = f"A\nF\n{politica}\n{episodios}\nMS {ficheiro_simulacao}"
    texto_simulacao = f"20\n150\nAG {ficheiro_agente}\n{ambiente}"
    texto_agente = f"1\n(0,0)\n0\nS (0,-1) (0,1) (1,0)\n{alpha}\n{gama}\n{eps_inicial}\n{eps_final}"

    with open(ficheiro_controlador, "w", encoding="utf-8") as f:
        f.write(texto_controlador)
    with open(ficheiro_simulacao, "w", encoding="utf-8") as f:
        f.write(texto_simulacao)
    with open("../agentes/" + ficheiro_agente, "w", encoding="utf-8") as f:
        f.write(texto_agente)

def resetRecolecaoReforco(ficheiro_controlador, ficheiro_simulacao, ficheiro_agente, politica,ambiente,tempo,episodios,alpha,gama,eps_inicial,eps_final):
    texto_controlador = f"A\nR {tempo}\n{politica}\n{episodios}\nMS {ficheiro_simulacao}"
    texto_simulacao = f"20\n150\nAG {ficheiro_agente}\n{ambiente}"
    texto_agente = f"1\n(0,0)\n0\nS (0,-1) (0,1) (1,0)\n{alpha}\n{gama}\n{eps_inicial}\n{eps_final}"

    with open(ficheiro_controlador, "w", encoding="utf-8") as f:
        f.write(texto_controlador)
    with open(ficheiro_simulacao, "w", encoding="utf-8") as f:
        f.write(texto_simulacao)
    with open("../agentes/" + ficheiro_agente, "w", encoding="utf-8") as f:
        f.write(texto_agente)


def changeTest(ficheiro_controlador):
    with open(ficheiro_controlador, "r", encoding="utf-8") as f:
        linhas = f.readlines()
    linhas[0] = "T\n"
    with open(ficheiro_controlador, "w", encoding="utf-8") as f:
        f.writelines(linhas)