from controlador import criarControlador


def main():
    controlador = criarControlador("controladorGenetico_farol.txt")
    controlador.executa()


if __name__ == "__main__":
    main()