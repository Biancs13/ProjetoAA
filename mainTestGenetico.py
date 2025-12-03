from motorSimulacao import MotorSimulacao

def main():
    motor = MotorSimulacao.criaGenetico("controladorGenetico.txt")
    motor.executa()

if __name__ == "__main__":
    main()


