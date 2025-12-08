from controlador import criarControlador


def main():
    controlador = criarControlador("controladorAleatorio_farol.txt")
    controlador.executa()


if __name__ == "__main__":
    main()