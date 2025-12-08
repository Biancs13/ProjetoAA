from controlador import criarControlador


def main():
    controlador = criarControlador("controladorReforco_recolecao.txt")
    controlador.executar()


if __name__ == "__main__":
    main()