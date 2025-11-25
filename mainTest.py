from motorSimulacao import MotorSimulacao, cria


def main():
    motor = cria("simulacao_farol.txt")
    motor.executa()

if __name__ == "__main__":
    main()