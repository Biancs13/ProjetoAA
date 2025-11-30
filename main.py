from time import sleep

from ambientes import Ambiente
from objetos.elemento import Elemento
from objetos.posicao import Posicao
from agentes.agente import Agente
from objetos.sensor import Sensor
from objetos.vetor import Vetor


def main():
    MAX_GRID = 5
    cheguei = False
    ambiente = Ambiente(MAX_GRID)
    elemento = Elemento("farol",10)
    ambiente.adicionar(elemento, Posicao(3,3))
    agente = Agente(1, Posicao(0,0),0)
    agente.instala(Sensor([Vetor(1,1),Vetor(1,-1),Vetor(1,0)]))
    print(representa(ambiente,agente,[]))
    while not cheguei:
        agente.ageAleatorio(MAX_GRID)
        observacao,posicoes = ambiente.observacaoParaAgente(agente)
        print( " ".join(str(p) for p in posicoes))
        print(agente)
        if agente.getPosicao() == Posicao(3,3):
            cheguei = True
            print("Cheguei ao farol")
        print(representa(ambiente,agente,posicoes))
        sleep(1)



#Depois pôr no motor de Simulação
def representa(ambiente,agente,posicoes):
    pos = agente.getPosicao()
    linhas = []
    for y in range(ambiente.tamanhoGrelha):
        linha = []
        for x in range(ambiente.tamanhoGrelha):
            if pos == Posicao(x, y):
                linha.append("A")
            elif Posicao(x,y) in posicoes:
                linha.append("*")
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