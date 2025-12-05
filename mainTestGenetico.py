from motorSimulacao import MotorSimulacao

def main():
    motor = MotorSimulacao.criaGenetico("controladorGenetico_farol.txt")
    motor.executa()

if __name__ == "__main__":
    main()


