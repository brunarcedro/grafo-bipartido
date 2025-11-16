# -*- coding: utf-8 -*-
"""
Algoritmo de Verificação de Grafo Bipartido
Tema: Relacionamento Usuários-Filmes

Um grafo bipartido divide os vértices em dois conjuntos disjuntos (V1 e V2)
onde todas as arestas conectam vértices de V1 a V2.

Aplicação: Sistema de Recomendação de Filmes
- V1: Usuários
- V2: Filmes
- Arestas: Usuário assistiu/avaliou o filme
"""
"""
Autoras: Larissa Paganini e Bruna Cedro
Disciplina: Tópicos de Programação Avançada
Ano: 2024
"""



from collections import deque, defaultdict
from typing import Dict, List, Tuple, Set


class GrafoBipartido:
    """
    Implementação de um Grafo Bipartido usando lista de adjacências
    """

    def __init__(self):
        self.grafo = defaultdict(list)
        self.vertices = set()
        self.usuarios = set()
        self.filmes = set()

    def adicionar_aresta(self, usuario: str, filme: str):
        """Adiciona uma aresta entre usuário e filme"""
        self.grafo[usuario].append(filme)
        self.grafo[filme].append(usuario)
        self.vertices.add(usuario)
        self.vertices.add(filme)
        self.usuarios.add(usuario)
        self.filmes.add(filme)

    def carregar_de_arquivo(self, arquivo: str):
        """
        Carrega o grafo de um arquivo texto
        Formato: USUARIO,FILME
        """
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                for linha in f:
                    linha = linha.strip()
                    if linha and not linha.startswith('#'):
                        partes = linha.split(',')
                        if len(partes) == 2:
                            usuario, filme = partes[0].strip(), partes[1].strip()
                            self.adicionar_aresta(usuario, filme)
            print(f"Grafo carregado com sucesso!")
            print(f"Usuários: {len(self.usuarios)}, Filmes: {len(self.filmes)}")
        except FileNotFoundError:
            print(f"Erro: Arquivo '{arquivo}' não encontrado!")
        except Exception as e:
            print(f"Erro ao carregar arquivo: {e}")

    def eh_bipartido_bfs(self) -> Tuple[bool, Dict[str, int]]:
        """
        Verifica se o grafo é bipartido usando BFS (Busca em Largura)
        Usa coloração de vértices: 0 (não visitado), 1 (cor A), 2 (cor B)

        Retorna:
            - bool: True se é bipartido, False caso contrário
            - dict: Mapeamento de vértice -> cor
        """
        cor = {vertice: 0 for vertice in self.vertices}
        passos = []  # Para demonstração do algoritmo

        # Pode ter componentes desconexos, então verificamos todos os vértices
        for vertice_inicial in self.vertices:
            if cor[vertice_inicial] == 0:  # Ainda não visitado
                # Inicializa BFS
                fila = deque([vertice_inicial])
                cor[vertice_inicial] = 1  # Primeira cor

                passos.append(f"Iniciando BFS a partir de '{vertice_inicial}'")
                passos.append(f"Colorindo '{vertice_inicial}' com cor 1 (Conjunto V1)")

                while fila:
                    u = fila.popleft()
                    passos.append(f"\nProcessando vértice '{u}' (cor {cor[u]})")

                    # Verifica todos os adjacentes
                    for v in self.grafo[u]:
                        if cor[v] == 0:  # Ainda não visitado
                            # Atribui cor oposta
                            cor[v] = 3 - cor[u]  # Se u=1, então v=2; se u=2, então v=1
                            fila.append(v)
                            passos.append(f"  → Colorindo '{v}' com cor {cor[v]} (Conjunto V{cor[v]})")
                        elif cor[v] == cor[u]:
                            # Mesma cor que o adjacente = NÃO é bipartido
                            passos.append(f"  ✗ CONFLITO: '{v}' tem a mesma cor que '{u}'!")
                            passos.append(f"\n⚠ GRAFO NÃO É BIPARTIDO!")
                            return False, cor, passos

        passos.append(f"\n✓ GRAFO É BIPARTIDO!")
        return True, cor, passos

    def obter_particao(self, cor: Dict[str, int]) -> Tuple[Set[str], Set[str]]:
        """
        Retorna os dois conjuntos da partição bipartida
        """
        v1 = {v for v, c in cor.items() if c == 1}
        v2 = {v for v, c in cor.items() if c == 2}
        return v1, v2

    def recomendar_filmes(self, usuario: str, cor: Dict[str, int]) -> List[str]:
        """
        Recomenda filmes para um usuário baseado em usuários similares
        (usuários que assistiram filmes em comum)
        """
        if usuario not in self.usuarios:
            return []

        # Filmes que o usuário já assistiu
        filmes_assistidos = set(self.grafo[usuario])

        # Encontra usuários que assistiram filmes em comum
        usuarios_similares = set()
        for filme in filmes_assistidos:
            for outro_usuario in self.grafo[filme]:
                if outro_usuario != usuario and outro_usuario in self.usuarios:
                    usuarios_similares.add(outro_usuario)

        # Encontra filmes que usuários similares assistiram mas o usuário não
        recomendacoes = set()
        for outro_usuario in usuarios_similares:
            for filme in self.grafo[outro_usuario]:
                if filme not in filmes_assistidos and filme in self.filmes:
                    recomendacoes.add(filme)

        return list(recomendacoes)

    def exibir_estatisticas(self):
        """Exibe estatísticas do grafo"""
        print("\n" + "="*50)
        print("ESTATÍSTICAS DO GRAFO")
        print("="*50)
        print(f"Total de vértices: {len(self.vertices)}")
        print(f"  - Usuários: {len(self.usuarios)}")
        print(f"  - Filmes: {len(self.filmes)}")

        total_arestas = sum(len(adj) for adj in self.grafo.values()) // 2
        print(f"Total de arestas: {total_arestas}")

        if self.usuarios:
            media = sum(len(self.grafo[u]) for u in self.usuarios) / len(self.usuarios)
            print(f"Média de filmes por usuário: {media:.2f}")


def main():
    """Função principal para teste do algoritmo"""
    print("="*50)
    print("VERIFICAÇÃO DE GRAFO BIPARTIDO")
    print("Tema: Sistema de Recomendação Usuários-Filmes")
    print("="*50)

    # Cria o grafo
    grafo = GrafoBipartido()

    # Carrega de arquivo
    arquivo = input("\nDigite o nome do arquivo (ex: exemplo1.txt): ").strip()
    if not arquivo:
        arquivo = "exemplo1.txt"

    grafo.carregar_de_arquivo(arquivo)

    # Exibe estatísticas
    grafo.exibir_estatisticas()

    # Verifica se é bipartido
    print("\n" + "="*50)
    print("EXECUTANDO ALGORITMO DE VERIFICAÇÃO")
    print("="*50)

    eh_bipartido, cor, passos = grafo.eh_bipartido_bfs()

    # Exibe os passos do algoritmo
    print("\nPASSOS DO ALGORITMO:")
    print("-"*50)
    for passo in passos:
        print(passo)

    # Resultado
    print("\n" + "="*50)
    if eh_bipartido:
        print("✓ RESULTADO: O grafo É BIPARTIDO")
        print("="*50)

        v1, v2 = grafo.obter_particao(cor)
        print(f"\nConjunto V1 (cor 1): {sorted(v1)}")
        print(f"Conjunto V2 (cor 2): {sorted(v2)}")

        # Verifica se a divisão é correta
        usuarios_v1 = v1 & grafo.usuarios
        filmes_v1 = v1 & grafo.filmes
        usuarios_v2 = v2 & grafo.usuarios
        filmes_v2 = v2 & grafo.filmes

        print(f"\nDivisão correta:")
        print(f"  V1: {len(usuarios_v1)} usuários, {len(filmes_v1)} filmes")
        print(f"  V2: {len(usuarios_v2)} usuários, {len(filmes_v2)} filmes")

        # Sistema de recomendação
        print("\n" + "="*50)
        print("SISTEMA DE RECOMENDAÇÃO")
        print("="*50)

        if grafo.usuarios:
            usuario_teste = list(grafo.usuarios)[0]
            print(f"\nFilmes assistidos por '{usuario_teste}':")
            print(f"  {list(grafo.grafo[usuario_teste])}")

            recomendacoes = grafo.recomendar_filmes(usuario_teste, cor)
            print(f"\nRecomendações para '{usuario_teste}':")
            if recomendacoes:
                for filme in recomendacoes:
                    print(f"  → {filme}")
            else:
                print("  (Nenhuma recomendação disponível)")
    else:
        print("✗ RESULTADO: O grafo NÃO É BIPARTIDO")
        print("="*50)
        print("\n⚠ Este grafo possui um ciclo ímpar!")
        print("Isso significa que não é possível dividir os vértices")
        print("em dois conjuntos disjuntos.")


if __name__ == "__main__":
    main()
