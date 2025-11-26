from motorSimulacao import MotorSimulacao, cria


def main():
    motor = cria("simulacao_recolecao.txt")
    print(motor)
    motor.executa()

if __name__ == "__main__":
    main()