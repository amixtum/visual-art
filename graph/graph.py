from math import inf
from queue import Queue
from random import choice


class graph:
    def __init__(self) -> None:
        self.graph = {}
        self.dfs_label = 0
        self.current_source_vertex = None
        self.finishing_time = 0

    def add_vertex(self, vertex) -> None:
        self.graph[vertex] = []
    
    def remove_vertex(self, vertex):
        self.graph.pop(vertex)
        for adj_list in self.graph.values:
            while vertex in adj_list:
                adj_list.remove(vertex)
    
    def add_edge(self, from_vertex, to_vertex):
        self.graph[from_vertex].append(to_vertex)
    
    def add_edge_undirected(self, from_vertex, to_vertex):
        self.add_edge(from_vertex, to_vertex)
        self.add_edge(to_vertex, from_vertex)
    
    def remove_edge(self, from_vertex, to_vertex):
        self.graph[from_vertex].remove(to_vertex)

    def remove_edge_undirected(self, from_vertex, to_vertex):
        self.remove_edge(self, from_vertex, to_vertex)
        self.remove_edge(self, to_vertex, from_vertex)
    
    def vertices(self) -> list:
        return self.graph.keys

    def edges(self, vertex) -> list:
        return self.graph[vertex]
    
    def edges_inward(self, vertex) -> list:
        edges = []
        for v in self.vertices():
            for edge in self.edges(v):
                if edge == vertex:
                    edges.append(v)
        return edges

    
    def count_vertices(self):
        return len(self.graph.keys)
    
    def count_edges(self):
        return sum([len(adj_list) for adj_list in self.graph.values])

    def degree(self, vertex):
        d = 0
        for v in self.graph.items:
            if v[0] != vertex:
                for e in v[1]:
                    if e == vertex:
                        d += 1
        return d

    def copy(self):
        c = graph()
        for vertex in self.graph.keys:
            c.add_vertex(vertex)
        for vertex in self.graph.keys:
            for edge in self.graph[vertex]:
                c.add_edge(vertex, edge)
        return c 

    def dfs(self, start_vertex, visited: dict = {}, connected: list = [], labels: dict = {}, finishing_times: dict = {}):
        if len(visited) == 0:
            for vertex in self.vertices():
                visited[vertex] = False

        visited[start_vertex] = True
        connected.append(start_vertex)

        for edge in self.edges(start_vertex):
            if not visited[edge]:
                self.dfs(edge, visited, connected, labels)
        
        labels[start_vertex] = self.dfs_label
        self.dfs_label -= 1

        self.finishing_time += 1
        finishing_times[start_vertex] = self.finishing_time
        
        return connected

    def topological_sort(self, start_vertex):
        self.finishing_time = 0
        visited = {}
        labels = {}
        finishing_times = {}
        for vertex in self.vertices():
            visited[vertex] = False

        self.dfs_label = len(self.vertices()) - 1

        for vertex in self.vertices():
            if not visited[vertex]:
                self.current_source_vertex = vertex
                self.dfs(start_vertex, visited=visited, connected=[], labels=labels, finishing_times=finishing_times)
        
        return labels

    def bfs(self, start_vertex):
        to_search = Queue()
        visited = {}
        distance = {}
        connected_component = []

        for vertex in self.vertices():
            visited[vertex] = False
            distance[vertex] = inf
        visited[start_vertex] = True
        distance[start_vertex] = 0
        to_search.put(start_vertex)

        while not to_search.empty():
            vertex = to_search.get()
            connected_component.append(vertex)
            for edge in self.edges(vertex):
                if not visited[edge]:
                    distance[edge] = distance[vertex] + 1
                    visited[edge] = True
                    to_search.put(edge)

        return connected_component
        
    
    def bfs_all(self, start_vertex):
        to_search = Queue()
        visited = {}
        distance = {}
        connected_component = []

        for vertex in self.vertices():
            visited[vertex] = False
            distance[vertex] = inf
        visited[start_vertex] = True
        distance[start_vertex] = 0
        to_search.put(start_vertex)

        while not to_search.empty():
            vertex = to_search.get()
            connected_component.append(vertex)
            for edge in self.edges(vertex):
                if not visited[edge]:
                    distance[edge] = distance[vertex] + 1
                    visited[edge] = True
                    to_search.put(edge)
        
        unreachable = [vertex for vertex in distance.keys if distance[vertex] == inf]
        for u_vertex in unreachable:
            component = self.bfs(u_vertex) 
            for c_vertex in component:
                if c_vertex in connected_component:
                    for edge in self.edges_inward(c_vertex):
                        if edge not in connected_component:
                            connected_component.append(edge)
                    
        return connected_component

    def choose_random_edge(self):
        start = choice(self.graph.keys)
        end = choice(self.graph[start])
        return (start, end)

    def contract_random(self):
        random_edge = self.choose_random_edge()

        self.remove_edge(random_edge[0], random_edge[1])
        edges_to_absorb = self.edges(random_edge[1])
        for vertex in self.vertices():
            indices = []
            adjust = 0
            for index in range(len(self.edges(vertex))):
                if self.edges(vertex)[index] == random_edge[1]:
                    indices.append(index - adjust)
                    adjust += 1
            for index in indices:
                self.remove_edge(vertex, self.edges(vertex).pop(index))
                self.add_edge(vertex, random_edge[0])
        self.remove_vertex(random_edge[1])
        for e in edges_to_absorb:
            self.add_edge(random_edge[0], e)
        
        # remove self loops
        for _ in range(self.edges(random_edge[0]).count(random_edge[0])):
            self.remove_edge(random_edge[0], random_edge[0])

    def contract_random_undirected(self):
        random_edge = self.choose_random_edge()

        self.remove_edge_undirected(random_edge[0], random_edge[1])
        edges_to_absorb = self.edges(random_edge[1])
        self.remove_vertex(random_edge[1])
        for e in edges_to_absorb:
            self.add_edge_undirected(random_edge[0], e)
        
        # remove self loops
        while random_edge[0] in self.graph[random_edge[0]]:
            self.remove_edge_undirected(random_edge[0], random_edge[0])
    
    def get_random_cut(self):
        while self.count_vertices() > 2:
            self.contract_random()

        r = []
        for v in self.graph.keys:
            r.append(self.graph[v])
        return r
    
    def get_random_cut_undirected(self):
        while self.count_vertices() > 2:
            self.contract_random_undirected()

        r = []
        for v in self.graph.keys:
            r.append(self.graph[v])
        return r
