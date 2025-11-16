# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Script de Teste Simplificado
Verifica se todos os componentes do projeto estão funcionando
"""
"""
Autoras: Larissa Paganini e Bruna Cedro
Disciplina: Tópicos de Programação Avançada
Ano: 2024
"""



import os
import sys


def verificar_arquivo(arquivo, descricao):
    """Verifica se um arquivo existe"""
    existe = os.path.isfile(arquivo)
    status = "[OK]" if existe else "[FALHOU]"
    print(f"{status} {descricao}: {arquivo}")
    return existe


def testar_imports():
    """Testa se todas as bibliotecas necessárias estão instaladas"""
    print("\n" + "="*60)
    print("TESTANDO IMPORTS")
    print("="*60)

    libs = {
        'networkx': 'NetworkX',
        'matplotlib': 'Matplotlib',
        'tkinter': 'Tkinter'
    }

    sucesso = True
    for lib, nome in libs.items():
        try:
            __import__(lib)
            print(f"[OK] {nome} instalado")
        except ImportError:
            print(f"[FALHOU] {nome} NAO instalado")
            sucesso = False

    return sucesso


def testar_arquivos():
    """Verifica se todos os arquivos necessários existem"""
    print("\n" + "="*60)
    print("TESTANDO ARQUIVOS")
    print("="*60)

    arquivos = {
        'grafo_bipartido.py': 'Algoritmo principal',
        'visualizador.py': 'Interface grafica',
        'animacao.py': 'Gerador de animacao',
        'exemplo1.txt': 'Exemplo 1 (bipartido valido)',
        'exemplo2.txt': 'Exemplo 2 (NAO bipartido)',
        'exemplo3.txt': 'Exemplo 3 (expandido)',
        'README.md': 'Documentacao principal',
        'APRESENTACAO.md': 'Roteiro de apresentacao',
        'teste_de_mesa.md': 'Teste de mesa',
        'GUIA_USO.md': 'Guia de uso',
        'requirements.txt': 'Dependencias'
    }

    todos_ok = True
    for arquivo, descricao in arquivos.items():
        if not verificar_arquivo(arquivo, descricao):
            todos_ok = False

    return todos_ok


def testar_algoritmo():
    """Testa o algoritmo com os exemplos"""
    print("\n" + "="*60)
    print("TESTANDO ALGORITMO")
    print("="*60)

    try:
        from grafo_bipartido import GrafoBipartido

        # Teste 1: Exemplo bipartido
        print("\n-> Testando exemplo1.txt (deve ser bipartido)...")
        grafo1 = GrafoBipartido()
        grafo1.carregar_de_arquivo('exemplo1.txt')
        eh_bip1, cor1, passos1 = grafo1.eh_bipartido_bfs()

        if eh_bip1:
            print("  [OK] Resultado correto: E BIPARTIDO")
            v1, v2 = grafo1.obter_particao(cor1)
            print(f"    V1: {len(v1)} vertices")
            print(f"    V2: {len(v2)} vertices")
        else:
            print("  [FALHOU] ERRO: Deveria ser bipartido!")
            return False

        # Teste 2: Exemplo NÃO bipartido
        print("\n-> Testando exemplo2.txt (NAO deve ser bipartido)...")
        grafo2 = GrafoBipartido()
        grafo2.carregar_de_arquivo('exemplo2.txt')
        eh_bip2, cor2, passos2 = grafo2.eh_bipartido_bfs()

        if not eh_bip2:
            print("  [OK] Resultado correto: NAO E BIPARTIDO")
        else:
            print("  [FALHOU] ERRO: NAO deveria ser bipartido!")
            return False

        # Teste 3: Exemplo expandido
        print("\n-> Testando exemplo3.txt (deve ser bipartido)...")
        grafo3 = GrafoBipartido()
        grafo3.carregar_de_arquivo('exemplo3.txt')
        eh_bip3, cor3, passos3 = grafo3.eh_bipartido_bfs()

        if eh_bip3:
            print("  [OK] Resultado correto: E BIPARTIDO")
            print(f"    Total de usuarios: {len(grafo3.usuarios)}")
            print(f"    Total de filmes: {len(grafo3.filmes)}")
        else:
            print("  [FALHOU] ERRO: Deveria ser bipartido!")
            return False

        # Teste de recomendação
        print("\n-> Testando sistema de recomendacao...")
        if grafo3.usuarios:
            usuario = list(grafo3.usuarios)[0]
            recomendacoes = grafo3.recomendar_filmes(usuario, cor3)
            print(f"  [OK] Recomendacoes para '{usuario}': {len(recomendacoes)} filmes")

        return True

    except Exception as e:
        print(f"  [FALHOU] ERRO ao executar algoritmo: {e}")
        import traceback
        traceback.print_exc()
        return False


def testar_estrutura_dados():
    """Testa estruturas de dados básicas"""
    print("\n" + "="*60)
    print("TESTANDO ESTRUTURAS DE DADOS")
    print("="*60)

    try:
        from grafo_bipartido import GrafoBipartido

        grafo = GrafoBipartido()

        # Adiciona algumas arestas
        grafo.adicionar_aresta("U1", "F1")
        grafo.adicionar_aresta("U1", "F2")
        grafo.adicionar_aresta("U2", "F1")

        print(f"  Vertices: {len(grafo.vertices)} (esperado: 4)")
        print(f"  Usuarios: {len(grafo.usuarios)} (esperado: 2)")
        print(f"  Filmes: {len(grafo.filmes)} (esperado: 2)")

        if len(grafo.vertices) == 4 and len(grafo.usuarios) == 2 and len(grafo.filmes) == 2:
            print("  [OK] Estruturas de dados corretas")
            return True
        else:
            print("  [FALHOU] Estruturas de dados incorretas")
            return False

    except Exception as e:
        print(f"  [FALHOU] ERRO: {e}")
        return False


def gerar_relatorio():
    """Gera relatório final"""
    print("\n" + "="*60)
    print("RELATORIO FINAL")
    print("="*60)

    relatorio = {
        'Imports': testar_imports(),
        'Arquivos': testar_arquivos(),
        'Estruturas de Dados': testar_estrutura_dados(),
        'Algoritmo': testar_algoritmo()
    }

    print("\n" + "-"*60)
    print("RESUMO:")
    print("-"*60)

    todos_ok = True
    for teste, resultado in relatorio.items():
        status = "[OK] PASSOU" if resultado else "[FALHOU]"
        print(f"{teste:.<40} {status}")
        if not resultado:
            todos_ok = False

    print("-"*60)

    if todos_ok:
        print("\n*** TODOS OS TESTES PASSARAM! ***")
        print("\nO projeto esta pronto para:")
        print("  - Executar as demonstracoes")
        print("  - Gerar a animacao")
        print("  - Apresentar o trabalho")
        print("\nProximos passos:")
        print("  1. Instale as dependencias: pip install -r requirements.txt")
        print("  2. Execute: python visualizador.py")
        print("  3. Execute: python animacao.py")
        print("  4. Prepare os slides da apresentacao")
        return 0
    else:
        print("\n*** ALGUNS TESTES FALHARAM ***")
        print("\nVerifique:")
        print("  - Todas as bibliotecas estao instaladas?")
        print("    Comando: pip install -r requirements.txt")
        print("  - Todos os arquivos estao no diretorio?")
        print("  - Ha erros de sintaxe no codigo?")
        return 1


def main():
    """Função principal"""
    print("="*60)
    print("TESTE AUTOMATIZADO DO PROJETO")
    print("Grafo Bipartido - Sistema de Recomendacao")
    print("="*60)

    # Verifica o diretório atual
    print(f"\nDiretorio atual: {os.getcwd()}")

    # Executa testes
    resultado = gerar_relatorio()

    return resultado


if __name__ == "__main__":
    sys.exit(main())
