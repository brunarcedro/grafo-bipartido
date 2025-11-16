# -*- coding: utf-8 -*-
"""
Visualizador Gráfico para Grafo Bipartido
Usa Tkinter + NetworkX + Matplotlib para visualização interativa
"""
"""
Autoras: Larissa Paganini e Bruna Cedro
Disciplina: Tópicos de Programação Avançada
Ano: 2024
"""



import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import networkx as nx
from grafo_bipartido import GrafoBipartido


class VisualizadorGrafoBipartido:
    """Interface gráfica para visualizar e analisar grafos bipartidos"""

    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Grafo Bipartido - Usuários e Filmes")
        self.root.geometry("1200x800")

        self.grafo = None
        self.eh_bipartido = None
        self.cor = None
        self.passos = []

        self.criar_interface()

    def criar_interface(self):
        """Cria a interface gráfica"""

        # Frame superior - Controles
        frame_controles = ttk.Frame(self.root, padding="10")
        frame_controles.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(frame_controles, text="Arquivo:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)

        self.entry_arquivo = ttk.Entry(frame_controles, width=30)
        self.entry_arquivo.pack(side=tk.LEFT, padx=5)
        self.entry_arquivo.insert(0, "exemplo1.txt")

        ttk.Button(frame_controles, text="Procurar", command=self.procurar_arquivo).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_controles, text="Carregar Grafo", command=self.carregar_grafo).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_controles, text="Verificar Bipartição", command=self.verificar_bipartido).pack(side=tk.LEFT, padx=5)

        # Frame principal - dividido em 2 colunas
        frame_principal = ttk.Frame(self.root)
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Coluna esquerda - Visualização do grafo
        frame_esquerdo = ttk.LabelFrame(frame_principal, text="Visualização do Grafo", padding="10")
        frame_esquerdo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.figura = Figure(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.figura, master=frame_esquerdo)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Coluna direita - Informações e passos
        frame_direito = ttk.Frame(frame_principal)
        frame_direito.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Estatísticas
        frame_stats = ttk.LabelFrame(frame_direito, text="Estatísticas", padding="10")
        frame_stats.pack(fill=tk.X, pady=(0, 10))

        self.label_stats = tk.Label(frame_stats, text="Nenhum grafo carregado",
                                     justify=tk.LEFT, anchor="w", font=('Courier', 9))
        self.label_stats.pack(fill=tk.X)

        # Resultado
        frame_resultado = ttk.LabelFrame(frame_direito, text="Resultado", padding="10")
        frame_resultado.pack(fill=tk.X, pady=(0, 10))

        self.label_resultado = tk.Label(frame_resultado, text="",
                                         justify=tk.LEFT, font=('Arial', 11, 'bold'))
        self.label_resultado.pack()

        # Passos do algoritmo
        frame_passos = ttk.LabelFrame(frame_direito, text="Passos do Algoritmo (BFS)", padding="10")
        frame_passos.pack(fill=tk.BOTH, expand=True)

        self.text_passos = scrolledtext.ScrolledText(frame_passos, height=15,
                                                       font=('Courier', 9), wrap=tk.WORD)
        self.text_passos.pack(fill=tk.BOTH, expand=True)

    def procurar_arquivo(self):
        """Abre diálogo para selecionar arquivo"""
        arquivo = filedialog.askopenfilename(
            title="Selecionar arquivo de grafo",
            filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
        )
        if arquivo:
            self.entry_arquivo.delete(0, tk.END)
            self.entry_arquivo.insert(0, arquivo)

    def carregar_grafo(self):
        """Carrega o grafo do arquivo"""
        arquivo = self.entry_arquivo.get().strip()
        if not arquivo:
            messagebox.showerror("Erro", "Por favor, especifique um arquivo!")
            return

        self.grafo = GrafoBipartido()
        try:
            self.grafo.carregar_de_arquivo(arquivo)
            self.atualizar_estatisticas()
            self.desenhar_grafo()
            messagebox.showinfo("Sucesso", "Grafo carregado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar grafo:\n{e}")

    def atualizar_estatisticas(self):
        """Atualiza as estatísticas exibidas"""
        if not self.grafo:
            return

        total_arestas = sum(len(adj) for adj in self.grafo.grafo.values()) // 2
        media_filmes = 0
        if self.grafo.usuarios:
            media_filmes = sum(len(self.grafo.grafo[u]) for u in self.grafo.usuarios) / len(self.grafo.usuarios)

        stats = f"""Total de vértices: {len(self.grafo.vertices)}
  • Usuários: {len(self.grafo.usuarios)}
  • Filmes: {len(self.grafo.filmes)}
Total de arestas: {total_arestas}
Média de filmes/usuário: {media_filmes:.2f}"""

        self.label_stats.config(text=stats)

    def desenhar_grafo(self, destacar_cores=False):
        """Desenha o grafo usando NetworkX e Matplotlib"""
        if not self.grafo:
            return

        self.figura.clear()
        ax = self.figura.add_subplot(111)

        # Cria grafo NetworkX
        G = nx.Graph()
        for vertice in self.grafo.vertices:
            G.add_node(vertice)
        for u in self.grafo.grafo:
            for v in self.grafo.grafo[u]:
                G.add_edge(u, v)

        # Layout bipartido
        usuarios = list(self.grafo.usuarios)
        filmes = list(self.grafo.filmes)

        pos = {}
        # Posiciona usuários à esquerda
        for i, usuario in enumerate(usuarios):
            pos[usuario] = (0, i * 2)

        # Posiciona filmes à direita
        for i, filme in enumerate(filmes):
            pos[filme] = (3, i * 2)

        # Cores dos nós
        if destacar_cores and self.cor:
            cores_nos = []
            for node in G.nodes():
                if self.cor.get(node) == 1:
                    cores_nos.append('#FF6B6B')  # Vermelho claro
                elif self.cor.get(node) == 2:
                    cores_nos.append('#4ECDC4')  # Azul claro
                else:
                    cores_nos.append('#95E1D3')  # Verde claro
        else:
            cores_nos = ['#FF6B6B' if node in self.grafo.usuarios else '#4ECDC4'
                         for node in G.nodes()]

        # Desenha o grafo
        nx.draw_networkx_nodes(G, pos, node_color=cores_nos, node_size=800, ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold', ax=ax)
        nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.6, ax=ax)

        # Legendas
        if destacar_cores and self.eh_bipartido:
            ax.text(0.02, 0.98, '● Conjunto V1', transform=ax.transAxes,
                    color='#FF6B6B', fontsize=10, weight='bold', va='top')
            ax.text(0.02, 0.93, '● Conjunto V2', transform=ax.transAxes,
                    color='#4ECDC4', fontsize=10, weight='bold', va='top')
        else:
            ax.text(0.02, 0.98, '● Usuários', transform=ax.transAxes,
                    color='#FF6B6B', fontsize=10, weight='bold', va='top')
            ax.text(0.02, 0.93, '● Filmes', transform=ax.transAxes,
                    color='#4ECDC4', fontsize=10, weight='bold', va='top')

        ax.set_title("Grafo Bipartido: Usuários ↔ Filmes", fontsize=14, weight='bold')
        ax.axis('off')
        self.canvas.draw()

    def verificar_bipartido(self):
        """Executa o algoritmo de verificação de bipartição"""
        if not self.grafo:
            messagebox.showerror("Erro", "Por favor, carregue um grafo primeiro!")
            return

        # Executa o algoritmo
        self.eh_bipartido, self.cor, self.passos = self.grafo.eh_bipartido_bfs()

        # Atualiza resultado
        if self.eh_bipartido:
            self.label_resultado.config(
                text="✓ O GRAFO É BIPARTIDO",
                fg='green'
            )
            v1, v2 = self.grafo.obter_particao(self.cor)
            resultado_extra = f"\n\nConjunto V1: {len(v1)} vértices\nConjunto V2: {len(v2)} vértices"
            self.label_resultado.config(text=self.label_resultado.cget('text') + resultado_extra)
        else:
            self.label_resultado.config(
                text="✗ O GRAFO NÃO É BIPARTIDO\n(possui ciclo ímpar)",
                fg='red'
            )

        # Atualiza passos
        self.text_passos.delete(1.0, tk.END)
        self.text_passos.insert(tk.END, "\n".join(self.passos))

        # Redesenha com cores
        self.desenhar_grafo(destacar_cores=True)


def main():
    """Função principal"""
    root = tk.Tk()
    app = VisualizadorGrafoBipartido(root)
    root.mainloop()


if __name__ == "__main__":
    main()
