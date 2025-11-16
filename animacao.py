# -*- coding: utf-8 -*-
"""
Gerador de Animação do Algoritmo de Grafo Bipartido
Cria uma animação mostrando passo a passo a execução do BFS
"""
"""
Autoras: Larissa Paganini e Bruna Cedro
Disciplina: Tópicos de Programação Avançada
Ano: 2024
"""



import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
import networkx as nx
from grafo_bipartido import GrafoBipartido


class AnimadorBipartido:
    """Cria animação da execução do algoritmo"""

    def __init__(self, arquivo_grafo):
        self.grafo = GrafoBipartido()
        self.grafo.carregar_de_arquivo(arquivo_grafo)

        # Executa o algoritmo para obter os passos
        self.eh_bipartido, self.cores_finais, self.passos = self.grafo.eh_bipartido_bfs()

        # Cria grafo NetworkX
        self.G = nx.Graph()
        for vertice in self.grafo.vertices:
            self.G.add_node(vertice)
        for u in self.grafo.grafo:
            for v in self.grafo.grafo[u]:
                self.G.add_edge(u, v)

        # Layout
        self.pos = self._criar_layout()

        # Estados para animação
        self.estados_cores = []
        self.textos_passos = []
        self._processar_passos()

    def _criar_layout(self):
        """Cria layout bipartido"""
        usuarios = sorted(list(self.grafo.usuarios))
        filmes = sorted(list(self.grafo.filmes))

        pos = {}
        # Usuários à esquerda
        for i, usuario in enumerate(usuarios):
            pos[usuario] = (0, i * 1.5)

        # Filmes à direita
        for i, filme in enumerate(filmes):
            pos[filme] = (5, i * 1.5)

        return pos

    def _processar_passos(self):
        """Processa os passos do algoritmo para criar estados de animação"""
        cores_atuais = {v: 'lightgray' for v in self.G.nodes()}

        # Estado inicial
        self.estados_cores.append(cores_atuais.copy())
        self.textos_passos.append("Estado Inicial\nTodos os vértices não visitados")

        # Simula a execução novamente para capturar estados
        cor_num = {v: 0 for v in self.grafo.vertices}
        fila = []

        for vertice_inicial in sorted(self.grafo.vertices):
            if cor_num[vertice_inicial] == 0:
                # Começa BFS
                fila = [vertice_inicial]
                cor_num[vertice_inicial] = 1
                cores_atuais[vertice_inicial] = '#FF6B6B'

                self.estados_cores.append(cores_atuais.copy())
                self.textos_passos.append(f"Iniciando BFS em '{vertice_inicial}'\nCor 1 (V1) atribuída")

                while fila:
                    u = fila.pop(0)

                    for v in self.grafo.grafo[u]:
                        if cor_num[v] == 0:
                            cor_num[v] = 3 - cor_num[u]
                            cores_atuais[v] = '#FF6B6B' if cor_num[v] == 1 else '#4ECDC4'
                            fila.append(v)

                            self.estados_cores.append(cores_atuais.copy())
                            self.textos_passos.append(
                                f"Processando '{u}'\n"
                                f"Colorindo '{v}' com cor {cor_num[v]}"
                            )

        # Estado final
        if self.eh_bipartido:
            self.textos_passos.append("✓ GRAFO É BIPARTIDO!\n\nV1 (vermelho) e V2 (azul)")
        else:
            self.textos_passos.append("✗ GRAFO NÃO É BIPARTIDO!\n\nEncontrado ciclo ímpar")

    def criar_animacao(self, arquivo_saida='animacao_bipartido.mp4', fps=1):
        """Cria a animação e salva em arquivo"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        fig.suptitle('Algoritmo de Verificação de Grafo Bipartido - BFS', fontsize=16, weight='bold')

        def atualizar_frame(frame):
            ax1.clear()
            ax2.clear()

            # Painel esquerdo - Grafo
            if frame < len(self.estados_cores):
                cores_frame = [self.estados_cores[frame][node] for node in self.G.nodes()]

                nx.draw_networkx_nodes(self.G, self.pos, node_color=cores_frame,
                                       node_size=1200, ax=ax1)
                nx.draw_networkx_labels(self.G, self.pos, font_size=9,
                                        font_weight='bold', ax=ax1)
                nx.draw_networkx_edges(self.G, self.pos, width=2, alpha=0.5, ax=ax1)

                ax1.set_title(f'Visualização do Grafo - Passo {frame}/{len(self.estados_cores)-1}',
                              fontsize=12, weight='bold')
                ax1.axis('off')

                # Legendas
                legend_elements = [
                    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightgray',
                               markersize=10, label='Não visitado'),
                    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#FF6B6B',
                               markersize=10, label='Conjunto V1'),
                    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#4ECDC4',
                               markersize=10, label='Conjunto V2')
                ]
                ax1.legend(handles=legend_elements, loc='upper left')

                # Painel direito - Explicação
                ax2.text(0.5, 0.5, self.textos_passos[frame],
                         ha='center', va='center', fontsize=14,
                         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                         wrap=True)
                ax2.set_xlim(0, 1)
                ax2.set_ylim(0, 1)
                ax2.axis('off')
                ax2.set_title('Explicação do Passo', fontsize=12, weight='bold')

            return ax1, ax2

        # Cria animação
        num_frames = len(self.estados_cores)
        anim = animation.FuncAnimation(fig, atualizar_frame, frames=num_frames,
                                       interval=1000/fps, repeat=True)

        # Salva
        print(f"Gerando animação com {num_frames} frames...")
        print("Isso pode levar alguns minutos...")

        try:
            # Tenta salvar como MP4
            anim.save(arquivo_saida, writer='ffmpeg', fps=fps, dpi=100)
            print(f"✓ Animação salva em: {arquivo_saida}")
        except Exception as e:
            print(f"Erro ao salvar MP4: {e}")
            print("Tentando salvar como GIF...")
            try:
                arquivo_gif = arquivo_saida.replace('.mp4', '.gif')
                anim.save(arquivo_gif, writer='pillow', fps=fps)
                print(f"✓ Animação salva em: {arquivo_gif}")
            except Exception as e2:
                print(f"Erro ao salvar GIF: {e2}")
                print("Mostrando animação na tela...")
                plt.show()


def main():
    """Função principal"""
    print("="*60)
    print("GERADOR DE ANIMAÇÃO - ALGORITMO DE GRAFO BIPARTIDO")
    print("="*60)

    arquivo = input("\nArquivo de grafo (padrão: exemplo1.txt): ").strip()
    if not arquivo:
        arquivo = "exemplo1.txt"

    print(f"\nCarregando grafo de '{arquivo}'...")
    animador = AnimadorBipartido(arquivo)

    print(f"\nGrafo carregado:")
    print(f"  - {len(animador.grafo.usuarios)} usuários")
    print(f"  - {len(animador.grafo.filmes)} filmes")
    print(f"  - {len(animador.estados_cores)} passos de animação")

    arquivo_saida = input("\nNome do arquivo de saída (padrão: animacao_bipartido.mp4): ").strip()
    if not arquivo_saida:
        arquivo_saida = "animacao_bipartido.mp4"

    fps_input = input("FPS (quadros por segundo, padrão: 1): ").strip()
    fps = float(fps_input) if fps_input else 1.0

    animador.criar_animacao(arquivo_saida, fps)

    print("\n" + "="*60)
    print("Processo concluído!")
    print("="*60)


if __name__ == "__main__":
    main()
