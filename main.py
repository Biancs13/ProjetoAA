from controlador import criarControlador


def main():
    controlador = criarControlador("controladorAleatorio_farol.txt")
    controlador.executar()


if __name__ == "__main__":
    main()