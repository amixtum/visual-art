import heapq
from math import inf
from queue import Queue
from random import choice


class graph:
    def __init__(self):
        self.adjacency_matrix = {}
        self.adjacency_lists = {}
        self.edge_weights = {}
        self.dfs_label = 0
        self.current_source_vertex = None
        self.finishing_time = 0

    def add_vertex(self, vertex) -> None:
        self.adjacency_matrix[vertex] = {}

        self.adjacency_lists[vertex] = []

        for v in self.vertices():
            self.adjacency_matrix[vertex][v] = False
            self.adjacency_matrix[v][vertex] = False
    
    def remove_vertex(self, vertex):
        for v in self.vertices():
            for _ in range(self.adjacency_lists[v].count(vertex)):
                self.adjacency_lists[v].remove(vertex)

            self.adjacency_matrix[v].pop(vertex)

        self.adjacency_lists.pop(vertex)

        self.adjacency_matrix.pop(vertex)
    
    def add_edge(self, from_vertex, to_vertex, weight):
        self.adjacency_lists[from_vertex].append(to_vertex)

        self.adjacency_matrix[from_vertex][to_vertex] = True

        self.edge_weights[(from_vertex, to_vertex)] = weight
    
    def add_edge_undirected(self, from_vertex, to_vertex, weight):
        self.add_edge(from_vertex, to_vertex)
        self.add_edge(to_vertex, from_vertex)
        self.edge_weights[(from_vertex, to_vertex)] = weight
        self.edge_weights[(to_vertex, from_vertex)] = weight
    
    def remove_edge(self, from_vertex, to_vertex):
        self.adjacency_lists[from_vertex].remove(to_vertex)
        self.adjacency_matrix[from_vertex][to_vertex] = False

    def remove_edge_undirected(self, from_vertex, to_vertex):
        self.remove_edge(self, from_vertex, to_vertex)
        self.remove_edge(self, to_vertex, from_vertex)
        self.edge_weights.pop((from_vertex, to_vertex))
        self.edge_weights.pop((to_vertex, from_vertex))
    
    def vertices(self) -> list:
        return list(self.adjacency_matrix.keys())

    def edges(self, vertex) -> list:
        return self.adjacency_lists[vertex]
    
    def edges_inward(self, vertex) -> list:
        edges = []
        for v in self.vertices():
            if self.has_edge(v, vertex):
                edges.append(v)
        return edges
    
    def has_edge(self, from_vertex, to_vertex):
        return self.adjacency_matrix[from_vertex][to_vertex]
    
    def count_vertices(self):
        return len(self.adjacency_matrix.keys)
    
    def count_edges(self):
        return sum([len(adj_list) for adj_list in self.adjacency_matrix.values])

    def degree(self, vertex):
        return sum([self.edges(v).count(vertex) for v in self.vertices()])

    def weight(self, from_vertex, to_vertex):
        return self.edge_weights[(from_vertex, to_vertex)]

    def copy(self):
        c = graph()
        for vertex in self.adjacency_matrix.keys:
            c.add_vertex(vertex)
        for vertex in self.adjacency_matrix.keys:
            for edge in self.adjacency_matrix[vertex]:
                c.add_edge(vertex, edge)
        return c 
    
    # not working
    def dfs(self, start_vertex, visited: dict = {}, connected: list = [], labels: dict = {}, finishing_times: dict = {}):
        if len(visited) == 0:
            for vertex in self.vertices():
                visited[vertex] = False

        if not visited[start_vertex]:
            visited[start_vertex] = True
            connected.append(start_vertex)
            for edge in self.edges(start_vertex):
                if not visited[edge]:
                    self.dfs(edge, visited, connected, labels, finishing_times)
        
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
        start = choice(list(self.adjacency_lists.keys()))
        end = choice(self.adjacency_lists[start])
        return (start, end)

    def contract_random(self):
        random_edge = self.choose_random_edge()

        self.remove_edge(random_edge[0], random_edge[1])
        edges_to_absorb = self.edges(random_edge[1])
        for vertex in self.vertices():
            w = 0
            for _ in range(self.edges(vertex).count(random_edge[1])):
                w += self.weight(vertex, random_edge[1])
                self.remove_edge(vertex, random_edge[1])
                self.add_edge(vertex, random_edge[0], w)

        w = 0
        for e in edges_to_absorb:
            w += self.weight(random_edge[1], e)
            self.remove_edge(random_edge[1], e)
            self.add_edge(random_edge[0], e, w)
        self.remove_vertex(random_edge[1])
        
        # remove self loops
        for _ in range(self.edges(random_edge[0]).count(random_edge[0])):
            self.remove_edge(random_edge[0], random_edge[0])
    
    def contract_random_no_parallel(self):
        random_edge = self.choose_random_edge()

        self.remove_edge(random_edge[0], random_edge[1])
        edges_to_absorb = self.edges(random_edge[1])
        for vertex in self.vertices():
            w = 0
            has_edge = False
            for _ in range(self.edges(vertex).count(random_edge[1])):
                has_edge = True
                w += self.weight(vertex, random_edge[1])
                self.remove_edge(vertex, random_edge[1])
            if has_edge:
                self.add_edge(vertex, random_edge[0], w)

        w = 0
        for e in set(edges_to_absorb):
            w += self.weight(random_edge[1], e)
            self.remove_edge(random_edge[1], e)
            self.add_edge(random_edge[0], e, w)
        self.remove_vertex(random_edge[1])
        
        # remove self loops
        for _ in range(self.edges(random_edge[0]).count(random_edge[0])):
            self.remove_edge(random_edge[0], random_edge[0])

    def contract_random_undirected(self):
        random_edge = self.choose_random_edge()

        self.remove_edge_undirected(random_edge[0], random_edge[1])
        edges_to_absorb = self.edges(random_edge[1])
        for e in edges_to_absorb:
            self.remove_edge_undirected(random_edge[1], e)
            self.add_edge_undirected(random_edge[0], e)
        self.remove_vertex(random_edge[1])
        
        # remove self loops
        while random_edge[0] in self.adjacency_matrix[random_edge[0]]:
            self.remove_edge_undirected(random_edge[0], random_edge[0])
    
    def get_random_cut(self):
        while self.count_vertices() > 2:
            self.contract_random()

        r = []
        for v in self.adjacency_matrix.keys:
            r.append(self.adjacency_matrix[v])
        return r
    
    def get_random_cut_undirected(self):
        while self.count_vertices() > 2:
            self.contract_random_undirected()

        r = []
        for v in self.adjacency_matrix.keys:
            r.append(self.adjacency_matrix[v])
        return r

    # not sure if O(nlogn)
    def djikstra(self, start_vertex):
        processed = {}

        # heap
        unprocessed = []

        distances = {}

        key = {}

        finished = False

        for vertex in self.vertices():
            distances[vertex] = inf
            processed[vertex] = False
            key[vertex] = inf
        
        key[start_vertex] = 0
        processed[start_vertex] = True
        distances[start_vertex] = 0

        for end_vertex in self.edges(start_vertex):
            heapq.heappush(unprocessed, (distances[start_vertex] + self.weight(start_vertex, end_vertex), (start_vertex, end_vertex)))

        while not finished:
            if len(unprocessed) > 0:
                min_edge = heapq.heappop(unprocessed)[1]
                processed[min_edge[1]] = True
                distances[min_edge[1]] = distances[min_edge[0]] + self.weight(min_edge[0], min_edge[1])
                if distances[min_edge[1]] < key[min_edge[1]]:
                    key[min_edge[1]] = distances[min_edge[1]]

                for end_vertex in self.edges(min_edge[1]):
                    if not processed[end_vertex]:
                        distance = distances[min_edge[1]] + self.weight(min_edge[1], end_vertex)
                        if distance < key[end_vertex]:
                            key[end_vertex] = distance
                        heapq.heappush(unprocessed, (distance, (min_edge[1], end_vertex)))
            else:
                finished = True
                        
        return key
