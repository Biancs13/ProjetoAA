

from controladorGenetico import criaGenetico, ControladorGenetico


def ler(nome):
    with open(nome, "r") as fich:
        return [linha.strip() for linha in fich.readlines()]


def criarControlador(ficheiro):
    conteudo = ler(ficheiro)
    modo = conteudo[0]
    problema = conteudo[1]
    politica = conteudo[2]
    if politica == "genetico":
        return criaGenetico(modo, problema, conteudo[3:])
    return None


'''  
    if tipo_politica == "reforco":
        return criaReforco(ficheiro)
'''


def main():
    controlador = criarControlador("controladorGenetico_recolecao.txt")
    controlador.executar()


if __name__ == "__main__":
    main()