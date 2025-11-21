from time import sleep

from ambiente import Ambiente
from elemento import Elemento
from posicao import Posicao
from agente import Agente


def main():
    MAX_GRID = 5
    cheguei = False
    ambiente = Ambiente(MAX_GRID)
    elemento = Elemento("farol",10)
    ambiente.adicionar(elemento, Posicao(3,3))
    agente = Agente(1, Posicao(0,0),None,0)
    print(representa(ambiente,agente))
    while not cheguei:
        agente.ageAleatorio(MAX_GRID)
        print(agente)
        if agente.getPosicao() == Posicao(3,3):
            cheguei = True
            print("Cheguei ao farol")
        print(representa(ambiente,agente))
        sleep(1)



#Depois pôr no motor de Simulação
def representa(ambiente,agente):
    pos = agente.getPosicao()
    linhas = []
    for y in range(ambiente.tamanhoGrelha):
        linha = []
        for x in range(ambiente.tamanhoGrelha):
            if pos == Posicao(x, y):
                linha.append("A")
            else:
                elemento = ambiente.grelha[Posicao(x,y)]
                if elemento is None:
                    linha.append(".")
                else:
                    linha.append(str(elemento))
        linhas.append(" ".join(linha))
    return "\n".join(linhas)


if __name__ == "__main__":
    main()