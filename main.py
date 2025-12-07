

from controladorGenetico import criaGenetico, ControladorGenetico
from controladorReforco import criarReforco


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
    elif politica == "reforco":
        return criarReforco(modo, problema, conteudo[3:])
    return None


def main():
    controlador = criarControlador("controladorReforco_recolecao.txt")
    controlador.executar()


if __name__ == "__main__":
    main()