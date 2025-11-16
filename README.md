# Projeto: Verificação de Grafo Bipartido
## Tema: Sistema de Relacionamento Usuários-Filmes

### 📋 Descrição do Projeto

Este projeto implementa um algoritmo de verificação de **Grafo Bipartido** aplicado a um sistema de recomendação de filmes. Um grafo bipartido é aquele cujo conjunto de vértices V pode ser particionado em dois subconjuntos V1 e V2, onde toda aresta conecta um vértice de V1 a outro de V2.

### 🎯 Aplicação Prática

**Sistema de Recomendação de Filmes:**
- **V1 (Conjunto 1):** Usuários
- **V2 (Conjunto 2):** Filmes
- **Arestas:** Representam que um usuário assistiu/avaliou um filme

### 🔧 Estrutura do Projeto

```
grafo_bipartido/
├── grafo_bipartido.py      # Implementação do algoritmo
├── visualizador.py          # Interface gráfica
├── exemplo1.txt             # Grafo bipartido válido
├── exemplo2.txt             # Grafo NÃO bipartido (ciclo ímpar)
├── exemplo3.txt             # Grafo expandido para recomendações
├── requirements.txt         # Dependências Python
└── README.md               # Este arquivo
```

### 🚀 Como Executar

#### 1. Instalar dependências:
```bash
pip install -r requirements.txt
```

#### 2. Executar no modo console:
```bash
python grafo_bipartido.py
```

#### 3. Executar com interface gráfica:
```bash
python visualizador.py
```

### 📊 Formato dos Arquivos de Entrada

Os arquivos `.txt` devem seguir o formato:
```
USUARIO,FILME
```

Exemplo:
```
Alice,Matrix
Alice,Inception
Bob,Matrix
Bob,Avatar
```

Linhas iniciadas com `#` são comentários e serão ignoradas.

### 🧮 Algoritmo Implementado

**Verificação de Bipartição usando BFS (Busca em Largura)**

**Ideia:** Tentar colorir o grafo com 2 cores, onde vértices adjacentes têm cores diferentes.

**Passos:**
1. Inicializa todos os vértices como não visitados (cor 0)
2. Para cada componente desconexo:
   - Escolhe um vértice inicial e atribui cor 1
   - Usa BFS para percorrer o grafo
   - Para cada vértice visitado, atribui cor oposta aos seus adjacentes
   - Se um adjacente já tiver a mesma cor → NÃO é bipartido
3. Se conseguir colorir todo o grafo → É bipartido

**Complexidade:** O(V + E) onde V = vértices e E = arestas

### 📈 Casos de Teste

#### Exemplo 1 (exemplo1.txt)
- **Resultado esperado:** BIPARTIDO ✓
- **Descrição:** Grafo válido de usuários e filmes
- **V1:** Usuários (Alice, Bob, Carlos, Diana, Eduardo)
- **V2:** Filmes (Matrix, Inception, Interstellar, Avatar, Titanic)

#### Exemplo 2 (exemplo2.txt)
- **Resultado esperado:** NÃO BIPARTIDO ✗
- **Descrição:** Contém um ciclo ímpar (Alice→Matrix→Bob→Inception→Alice)
- **Motivo:** Viola a propriedade bipartida

#### Exemplo 3 (exemplo3.txt)
- **Resultado esperado:** BIPARTIDO ✓
- **Descrição:** Sistema expandido para demonstração de recomendações
- **Funcionalidade adicional:** Sistema de recomendação baseado em colaboração

### 🎓 Conceitos Teóricos

#### O que é um Grafo Bipartido?

Um grafo G = (V, E) é **bipartido** se:
- V pode ser particionado em V1 e V2
- V1 ∩ V2 = ∅ (conjuntos disjuntos)
- V1 ∪ V2 = V (cobrem todos os vértices)
- Toda aresta (u,v) ∈ E tem u ∈ V1 e v ∈ V2 (ou vice-versa)

#### Propriedade Importante:

**Teorema:** Um grafo é bipartido **se e somente se** não contém ciclos de comprimento ímpar.

#### Por que funciona?

- Se tentarmos colorir um ciclo ímpar com 2 cores alternadas, eventualmente teremos dois vértices adjacentes com a mesma cor
- Isso viola a propriedade de bipartição

### 🎬 Aplicações Práticas

1. **Sistemas de Recomendação** (este projeto)
   - Netflix, Amazon Prime, Spotify
   - Recomendar conteúdo baseado em usuários similares

2. **Matching de Empregos**
   - Candidatos ↔ Vagas
   - Encontrar a melhor combinação

3. **Redes Sociais**
   - Páginas ↔ Seguidores
   - Análise de comunidades

4. **Biologia**
   - Proteínas ↔ Doenças
   - Estudar interações moleculares

### 👥 Autores

Larissa Paganini e Bruna Cedro

### 📚 Referências

- Sedgewick, R. & Wayne, K. - Algorithms, 4th Edition
- Cormen et al. - Introduction to Algorithms (CLRS)
- NetworkX Documentation: https://networkx.org/

### 📝 Licença

Projeto acadêmico para disciplina de Tópicos de Programação Avançada.
