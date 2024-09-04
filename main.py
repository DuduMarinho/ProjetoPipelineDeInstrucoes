import tkinter as tk
from threading import Thread
import time
import random

class Processo:
    def __init__(self, nome, tempo_execucao, atualizar_gui_callback):
        self.nome = nome
        self.tempo_execucao = tempo_execucao
        self.atualizar_gui_callback = atualizar_gui_callback
        self.status = "Aguardando"

    def executar(self, linha):
        self.status = "Executando"
        for i in range(self.tempo_execucao):
            self.atualizar_gui_callback(linha, i, "green")
            time.sleep(1)  # Simula o tempo de execução
            if random.choice([True, False]):
                self.status = "Interrompido"
                self.atualizar_gui_callback(linha, i, "red")
                break
        else:
            self.status = "Concluído"
            self.atualizar_gui_callback(linha, self.tempo_execucao - 1,
                                        "blue")

class Pipeline:
    def __init__(self, processos, atualizar_gui_callback):
        self.processos = processos
        self.atualizar_gui_callback = atualizar_gui_callback

    def executar(self):
        for idx, processo in enumerate(self.processos):
            processo_thread = Thread(target=processo.executar, args=(idx,))
            processo_thread.start()
            processo_thread.join()  # Espera o processo terminar antes de iniciar o próximo


class AplicacaoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulação de Pipeline de Processador")

        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.grid(column=0, row=0, padx=20, pady=20)

        self.start_button = tk.Button(root, text="Iniciar", command=self.iniciar_simulacao)
        self.start_button.grid(column=0, row=1, padx=10, pady=10)

        self.linhas = []

    def criar_pipeline_visual(self, num_processos, max_ciclos):
        tamanho_quadrado = 30
        padding = 10
        self.linhas.clear()

        for i in range(num_processos):
            linha = []
            for j in range(max_ciclos):
                x1 = j * (tamanho_quadrado + padding) + padding
                y1 = i * (tamanho_quadrado + padding) + padding
                x2 = x1 + tamanho_quadrado
                y2 = y1 + tamanho_quadrado
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")
                linha.append(rect)
            self.linhas.append(linha)

    def atualizar_gui(self, linha, ciclo, cor):
        self.canvas.itemconfig(self.linhas[linha][ciclo], fill=cor)

    def iniciar_simulacao(self):
        num_processos = 6
        max_ciclos = 10
        self.criar_pipeline_visual(num_processos, max_ciclos)

        processos = [Processo(f"Processo {i + 1}", random.randint(5, 10), self.atualizar_gui) for i in
                     range(num_processos)]
        pipeline = Pipeline(processos, self.atualizar_gui)
        Thread(target=pipeline.executar).start()


if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacaoGUI(root)
    root.mainloop()
