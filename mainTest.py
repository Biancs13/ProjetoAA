from motorSimulacao import MotorSimulacao

def main():
    motor = MotorSimulacao("simulacao_farol.txt", modoAleatorio=True)
    motor.cria("simulacao_farol.txt")
    motor.executa()

if __name__ == "__main__":
    main()