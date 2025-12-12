import tkinter as tk

from objetos.posicao import Posicao

class GUI:
    def __init__(self, tamanho, tamanho_cell=15):
        self.tamanho = tamanho
        self.tamanho_cell = tamanho_cell

        self.root = tk.Tk()
        self.root.title("GUI")

        side = tamanho * tamanho_cell
        self.canvas = tk.Canvas(self.root, width=side, height=side, bg="white")
        self.canvas.pack()

    def representa(self, ambiente, agentes):
        self.canvas.delete("all")
        self.desenha_grelha()

        pos_agentes = [a.getPosicao() for a in agentes]
        pos_vistas = [pos for a in agentes for pos in ambiente.observacaoParaAgente(a)[1]]

        for y in range(self.tamanho):
            for x in range(self.tamanho):
                pos = Posicao(x, y)

                if pos in pos_agentes:
                    self._desenha_celula(x, y, "navy")
                    continue

                elemento = ambiente.getElemento(pos)

                if pos in pos_vistas:
                    if elemento is not None and elemento.isSolido():
                        pass
                    else:
                        self._desenha_celula(x, y, "lightblue")
                        continue

                nome = elemento.getNome()
                if nome == "Vazio":
                    continue
                if nome == "ninho":
                    cor = "lightcoral"
                elif nome == "farol":
                    cor = "yellow"
                elif elemento.isColetavel():
                    cor = "lightgreen"
                else:
                    cor = "gray"
                self._desenha_celula(x, y, cor)
        self.root.update()

    def desenha_grelha(self):
        for i in range(self.tamanho + 1):
            x = i * self.tamanho_cell
            self.canvas.create_line(x, 0, x, self.tamanho * self.tamanho_cell)
            self.canvas.create_line(0, x, self.tamanho * self.tamanho_cell, x)

    def _desenha_celula(self, x, y, cor):
        x0 = x * self.tamanho_cell
        y0 = y * self.tamanho_cell
        x1 = x0 + self.tamanho_cell
        y1 = y0 + self.tamanho_cell
        self.canvas.create_rectangle(x0, y0, x1, y1, fill=cor, outline="black")