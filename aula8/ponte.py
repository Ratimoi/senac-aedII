grafo = {
    'A': ['C', 'D', 'B'],
    'B': ['A', 'D'],
    'C': ['A', 'D'],
    'D': ['C', 'A', 'B'],
}

def dfs(grafo, v, visitados):
    visitados.add(v)
    print(v)
    for w in grafo[v]:
        if w not in visitados:
            dfs(grafo, w, visitados)

dfs(grafo, 'A', set())

