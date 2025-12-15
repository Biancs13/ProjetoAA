from controlador import criarControlador


def main():
    controlador = criarControlador("demo/controladorReforco_farol_s.txt")
    controlador.executa()


if __name__ == "__main__":
    main()