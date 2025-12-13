from controlador import criarControlador
from demo.configurarDemo import resetFarol, changeTest, ambiente_farol_sem_paredes
from construtorGraficos import grafico_passos   # ou onde isto estiver

# -------- TREINO --------
ficheiro_controlador = "controladorAleatorio_farol.txt"

resetFarol(
    ficheiro_controlador,
    "simulacao_farol_aleatorio.txt",
    "agente_aleatorio_farol.txt",
    "aleatorio",
    ambiente_farol_sem_paredes
)

controlador = criarControlador(ficheiro_controlador,100)

controlador.executa()

grafico_passos(controlador.numero_passos)


changeTest(ficheiro_controlador)
controlador = criarControlador(ficheiro_controlador)
controlador.executa()