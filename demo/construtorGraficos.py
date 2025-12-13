import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.axes_grid1 import make_axes_locatable
from objetos.acao import atuar
from objetos.posicao import Posicao


def construir_genetico(caminhos, motor, valores_f_r, passos):
    graficoCaminhos(caminhos, motor)
    grafico_fitness_recompensas(valores_f_r, "genetico")
    grafico_passos(passos)
    mapa = calcular_mapa(caminhos,motor.ambiente.tamanhoGrelha)
    criar_heatmap(mapa, motor, cmap="coolwarm", titulo="Heatmap de Visitas")


def construir_reforco(valores_f_r,passos,q):
    grafico_fitness_recompensas(valores_f_r, "genetico")
    grafico_passos(passos)
    criar_heatmap_ref(q, cmap="coolwarm", titulo="Heatmap de Q-table")



# CAMINHO
def reconstruir_caminho(posicao, angulo, comportamento):
    caminho = [posicao]
    for a in comportamento:
        posicao, angulo = atuar(posicao,angulo,a)
        caminho.append(posicao)
    return caminho

#MAPA
def calcular_mapa(caminhos,tamanho_grelha):
    mapa_visitas = {Posicao(x,y):0 for x in range(tamanho_grelha) for y in range(tamanho_grelha)}
    for c in caminhos:
        for pos in c:
            mapa_visitas[pos] = mapa_visitas[pos] + 1
    return mapa_visitas

#GRAFICOS
def graficoCaminhos(caminhos,motor):
    grelha_size = motor.ambiente.tamanhoGrelha
    fig, ax = plt.subplots(figsize=(grelha_size * 0.5, grelha_size * 0.5))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.set_xlim(0, grelha_size)
    ax.set_ylim(grelha_size, 0)
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    cmap = plt.get_cmap("rainbow")
    colors = cmap(np.linspace(0, 1, len(caminhos)))
    if len(caminhos) == 1:
        plot_gens = [0]
    else:
        indices = {0, len(caminhos)//2, len(caminhos)-1}
        plot_gens = sorted(list(indices))
    for i in plot_gens:
        path = caminhos[i]
        x_vals = [p.getX() for p in path]
        y_vals = [p.getY() for p in path]
        ax.plot(x_vals, y_vals, color=colors[i], alpha=0.7,
                label=f"Geração {i+1}", linewidth=2)
        if x_vals:
            ax.plot(x_vals[-1], y_vals[-1], 'x', color=colors[i],
                    markersize=10, markeredgewidth=2)
    for pos, ele in motor.ambiente.grelha.items():
        if ele.getId() != (-1, -1, -1):
            ax.text(
                pos.x,
                pos.y,
                str(ele) if hasattr(ele, "nome") else str(ele),
                fontsize=13,
                ha="center",
                va="center",
                color="black",
                fontweight="bold"
            )
    ax.set_title("Melhores Caminhos por Geração", pad=20)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.spines['bottom'].set_color('black')
    ax.spines['top'].set_color('black')
    ax.spines['left'].set_color('black')
    ax.spines['right'].set_color('black')
    ax.grid(True, color='lightgray', linestyle='--')
    ax.legend(loc='lower right')
    plt.show()

def grafico_fitness_recompensas(valores,tipo):
    plt.figure(figsize=(10, 5))
    plt.plot(range(len(valores)),valores, marker='o')
    if tipo == "reforco": mensagem = "Episodes"
    else: mensagem = "Generation"
    plt.title("Max Combined Fitness per " + mensagem)
    plt.xlabel(mensagem)
    plt.ylabel("Max Combined Fitness Score")
    plt.grid(True)
    plt.show()

def grafico_passos(passos):
    plt.figure(figsize=(10, 5))
    plt.plot(range(len(passos)), passos, marker='o')
    plt.title("Nº de Passos até à condição de fim")
    plt.xlabel("Nº repetições")
    plt.ylabel("Passos")
    plt.grid(True)
    plt.show()



#HEATMAP
def criar_heatmap(mapa, motor, cmap="coolwarm", titulo="Heatmap de Visitas"):
    coords = np.array([(p.x, p.y) for p in mapa.keys()])
    valores = np.array(list(mapa.values()))
    xs = coords[:, 0]
    ys = coords[:, 1]
    x_min, x_max = xs.min(), xs.max()
    y_min, y_max = ys.min(), ys.max()
    largura = x_max - x_min + 1
    altura = y_max - y_min + 1
    heatmap = np.zeros((altura, largura), dtype=float)
    heatmap[ys - y_min, xs - x_min] = valores
    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.imshow(
        heatmap,
        cmap=cmap,
        interpolation="nearest",
        aspect="equal",
        origin="upper"
    )
    plt.colorbar(im, label="Número de Visitas", fraction=0.046, pad=0.04)
    ax.set_xticks(np.arange(largura))
    ax.set_yticks(np.arange(altura))
    ax.set_xticklabels(np.arange(x_min, x_max + 1))
    ax.set_yticklabels(np.arange(y_min, y_max + 1))
    ax.set_xlabel("Posição X")
    ax.set_ylabel("Posição Y")
    ax.set_title(titulo)
    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')
    for pos, ele in motor.ambiente.grelha.items():
        if ele.getId() != (-1, -1, -1):
            ax.text(
                pos.x,
                pos.y,
                str(ele) if hasattr(ele, "nome") else str(ele),
                fontsize=20,
                ha="center",
                va="center",
                color="black",
                fontweight="bold"
            )
    ax.set_xticks(np.arange(-.5, largura, 1), minor=True)
    ax.set_yticks(np.arange(-.5, altura, 1), minor=True)
    ax.grid(which="minor", color="w", linestyle="-", linewidth=0.8)
    plt.tight_layout()
    plt.show()


def criar_heatmap_ref(q, cmap="coolwarm", titulo="Heatmap de Q-table"):
    data_flat = []
    for estado_tuple, dic_acoes in q.items():
        for acao, valor in dic_acoes.items():
            data_flat.append([estado_tuple, str(acao), valor])
    df = pd.DataFrame(data_flat, columns=['Estado_ID', 'Acao', 'ValorQ'])
    acoes = sorted(df['Acao'].unique())
    num_acoes = len(acoes)
    unique_states = sorted(df['Estado_ID'].unique())
    state_to_idx = {state_id: i for i, state_id in enumerate(unique_states)}
    num_estados_discretos = len(unique_states)
    heatmap_matrix = np.full((num_estados_discretos, num_acoes), np.nan)
    for _, row in df.iterrows():
        estado_idx = state_to_idx[row['Estado_ID']]
        acao_idx = acoes.index(row['Acao'])
        heatmap_matrix[estado_idx, acao_idx] = row['ValorQ']
    ponto_medio = num_estados_discretos // 2
    matrix_top = heatmap_matrix[:ponto_medio, :]
    matrix_bottom = heatmap_matrix[ponto_medio:, :]
    num_estados_top = matrix_top.shape[0]
    num_estados_bottom = matrix_bottom.shape[0]
    fig, (ax_top, ax_bottom) = plt.subplots(
        1, 2,
        figsize=(10, 10),
        sharey=False
    )
    fig.suptitle(titulo, fontsize=16)
    vmin_val = np.nanmin(heatmap_matrix) if not np.all(np.isnan(heatmap_matrix)) else 0
    vmax_val = np.nanmax(heatmap_matrix) if not np.all(np.isnan(heatmap_matrix)) else 1
    ax_top.imshow(
        matrix_top, cmap=cmap, interpolation="nearest", aspect="auto", origin="upper",
        vmin=vmin_val, vmax=vmax_val
    )
    ax_top.set_title(f"Parte Superior (Estados 1 a {ponto_medio})", fontsize=10)
    ax_top.set_xticks(np.arange(num_acoes))
    ax_top.xaxis.set_ticks_position('top')
    ax_top.xaxis.set_label_position('top')
    ax_top.set_xticklabels(acoes, rotation=45, ha="left")
    ax_top.set_xlabel("Ação")
    y_indices_top = np.arange(num_estados_top)
    y_labels_top = [str(i + 1) for i in y_indices_top]
    y_labels_esparsos_top = [''] * num_estados_top
    if num_estados_top > 0: y_labels_esparsos_top[0] = y_labels_top[0]
    if num_estados_top == num_estados_discretos and num_estados_top > 1: y_labels_esparsos_top[-1] = y_labels_top[-1]
    ax_top.set_yticks(y_indices_top)
    ax_top.set_yticklabels(y_labels_esparsos_top)
    ax_top.set_ylabel("Estado")
    ax_top.set_xticks(np.arange(-.5, num_acoes, 1), minor=True)
    ax_top.set_yticks(np.arange(-.5, num_estados_top, 1), minor=True)
    ax_top.grid(which="minor", color="k", linestyle="-", linewidth=0.5)
    ax_top.tick_params(which="minor", size=0)
    im_bottom = ax_bottom.imshow(
        matrix_bottom,
        cmap=cmap,
        interpolation="nearest",
        aspect="auto",
        origin="upper",
        vmin=vmin_val,
        vmax=vmax_val
    )
    ax_bottom.set_title(f"Parte Inferior (Estados {ponto_medio + 1} a {num_estados_discretos})", fontsize=10)
    ax_bottom.set_xticks(np.arange(num_acoes))
    ax_bottom.xaxis.set_ticks_position('top')
    ax_bottom.xaxis.set_label_position('top')
    ax_bottom.set_xticklabels(acoes, rotation=45, ha="left")
    ax_bottom.set_xlabel("Ação")
    y_indices_bottom = np.arange(num_estados_bottom)
    y_labels_bottom = [str(i + ponto_medio + 1) for i in y_indices_bottom]
    y_labels_esparsos_bottom = [''] * num_estados_bottom
    if num_estados_bottom > 0:
        y_labels_esparsos_bottom[0] = y_labels_bottom[0]
        y_labels_esparsos_bottom[-1] = y_labels_bottom[-1]
    ax_bottom.set_yticks(y_indices_bottom)
    ax_bottom.set_yticklabels(y_labels_esparsos_bottom)
    ax_bottom.set_ylabel("Estado")
    ax_bottom.set_xticks(np.arange(-.5, num_acoes, 1), minor=True)
    ax_bottom.set_yticks(np.arange(-.5, num_estados_bottom, 1), minor=True)
    ax_bottom.grid(which="minor", color="k", linestyle="-", linewidth=0.5)
    ax_bottom.tick_params(which="minor", size=0)
    cax = fig.add_axes([0.92, 0.05, 0.03, 0.9])
    fig.colorbar(im_bottom, cax=cax, label="Recompensa")
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()
