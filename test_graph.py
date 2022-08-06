from graph.graph import graph

g = graph()
g.add_vertex(1)
g.add_vertex(2)
g.add_vertex(3)
g.add_vertex(4)
g.add_vertex(5)

g.add_edge(1, 2, 1)
g.add_edge(1, 3, 3)
g.add_edge(2, 3, 1)
g.add_edge(2, 4, 2)
g.add_edge(3, 5, 1)
g.add_edge(4, 5, 3)
g.add_edge(4, 3, 4)
g.add_edge(5, 3, 4)
g.add_edge(5, 2, 2)

g.contract_random()

for v in g.vertices():
    print(g.djikstra(v))
    print(g.bfs(v))
    print(g.dfs(v))