import networkx as nx
import queue as q
import random
import math


NUM_INDIVID = 200
FUNCTION = lambda x: (1/math.exp(x))

class Function:
    def __init__(self, func:str) -> None:
        self._function = func
        
    def new_function(self, func: str)->None:
        self._function = func
        
    def mean(self, t: float)->None:
        return eval(self._function)

class Algorithm:
    def __init__(self) -> None:
        self._graph = nx.DiGraph()
        
        self._func_T = Function('0.999*t')
        self._start_T = 10.0**(15)
        self._end_T = 10.0**(-15)
        self._func_F = random.sample
        self._func_E = self.calculate_length
        self._func_swap = Function('(-1)*1/t')
        
    def init_graph(self, vertex_num: int, edges: list[dict])->None:
        
        self._graph.add_nodes_from([(x+1) for x in range(vertex_num)])
        for edge in edges:
            self._graph.add_edge(edge["from"], edge["to"], weight=edge["weight"])
            
            
    def search_hamilton_cycle(self) -> list[dict]:
        edges_way = self.search_first_way()
        if len(edges_way) == 0: return edges_way
        vertexes_way = [edge["from"] for edge in edges_way]
        min_length = self._func_E(edges_way)
        min_edges_way = edges_way.copy()      

        
        current_T = self._start_T
        while current_T > self._end_T:
            swap_vertexes = self._func_F(range(0, len(vertexes_way)), 2)
            new_vertexes_way, new_edges_way, is_swapped = self.swap_vertexes(swap_vertexes[0], swap_vertexes[1], vertexes_way.copy(), edges_way.copy())
            if not is_swapped:
                current_T = self._func_T.mean(current_T)
                continue
            
            length = self._func_E(edges_way)
            new_length = self._func_E(new_edges_way)
            if length > new_length:
                if min_length > new_length:
                    min_length = new_length
                    min_edges_way = new_edges_way.copy()

                vertexes_way = new_vertexes_way.copy()
                edges_way = new_edges_way.copy()
                
            else:
                if random.random() < math.exp(-(new_length - length + 1) / current_T):
                    vertexes_way = new_vertexes_way.copy()
                    edges_way = new_edges_way.copy()
            
            current_T = self._func_T.mean(current_T)

        return min_edges_way
    
    
    def search_first_way(self) -> list[dict]:
        individs = [Individ(self._graph) for _ in range(NUM_INDIVID)]
        for i in range(len(individs)): individs[i].algoritm()
        best_individ = min(individs, key= lambda ind: ind.way_long)
        return best_individ.way if best_individ.way_long < 10**6 else []
    
    def swap_vertexes(self, index_1: int, index_2: int, way_vertexes: list, way_edges: list[dict]) -> tuple[list, list[dict], bool]:
        index_1, index_2 = min(index_1, index_2), max(index_1, index_2)
        vertex_pred_1 = way_vertexes[(index_1 - 1 + len(way_vertexes)) % len(way_vertexes)]
        vertex_pred_2 = way_vertexes[(index_2 - 1 + len(way_vertexes)) % len(way_vertexes)]
        vertex_1 = way_vertexes[index_1]
        vertex_2 = way_vertexes[index_2]
        vertex_last_1 = way_vertexes[(index_1 + 1) % len(way_vertexes)]
        vertex_last_2 = way_vertexes[(index_2 + 1) % len(way_vertexes)]
        
        if vertex_pred_1 == vertex_2 or vertex_last_1 == vertex_2:
            if vertex_pred_1 == vertex_2:
                can_swap = (self._graph.has_edge(vertex_pred_2, vertex_1)
                            and self._graph.has_edge(vertex_2, vertex_last_1)
                            and self._graph.has_edge(vertex_1, vertex_2))
                
                if can_swap:
                    way_edges[(index_2 - 1 + len(way_vertexes)) % len(way_vertexes)] = \
                    {"from": vertex_pred_2, "to": vertex_1, "weight": self._graph[vertex_pred_2][vertex_1]["weight"]}
                    way_edges[index_2] = {"from": vertex_1, "to": vertex_2, "weight": self._graph[vertex_1][vertex_2]["weight"]}
                    way_edges[index_1] = {"from": vertex_2, "to": vertex_last_1, "weight": self._graph[vertex_2][vertex_last_1]["weight"]}
                    
            if vertex_last_1 == vertex_2:
                can_swap = (self._graph.has_edge(vertex_pred_1, vertex_2)
                            and self._graph.has_edge(vertex_1, vertex_last_2)
                            and self._graph.has_edge(vertex_2, vertex_1))
                
                if can_swap:
                    way_edges[(index_1 - 1 + len(way_vertexes)) % len(way_vertexes)] = \
                    {"from": vertex_pred_1, "to": vertex_2, "weight": self._graph[vertex_pred_1][vertex_2]["weight"]}
                    way_edges[index_1] = {"from": vertex_2, "to": vertex_1, "weight": self._graph[vertex_2][vertex_1]["weight"]}
                    way_edges[index_2] = {"from": vertex_1, "to": vertex_last_2, "weight": self._graph[vertex_1][vertex_last_2]["weight"]}
                      
        else:
            can_swap = (self._graph.has_edge(vertex_pred_1, vertex_2) 
                        and self._graph.has_edge(vertex_2, vertex_last_1) 
                        and self._graph.has_edge(vertex_pred_2, vertex_1) 
                        and self._graph.has_edge(vertex_1, vertex_last_2))

            if can_swap: 
                way_edges[(index_1 - 1 + len(way_vertexes)) % len(way_vertexes)] = \
                {"from": vertex_pred_1, "to": vertex_2, "weight": self._graph[vertex_pred_1][vertex_2]["weight"]}
                way_edges[index_1] = {"from": vertex_2, "to": vertex_last_1, "weight": self._graph[vertex_2][vertex_last_1]["weight"]}
                way_edges[(index_2 - 1 + len(way_vertexes)) % len(way_vertexes)] = \
                {"from": vertex_pred_2, "to": vertex_1, "weight": self._graph[vertex_pred_2][vertex_1]["weight"]}
                way_edges[index_2] = {"from": vertex_1, "to": vertex_last_2, "weight": self._graph[vertex_1][vertex_last_2]["weight"]}

        if can_swap: way_vertexes[index_1], way_vertexes[index_2] = way_vertexes[index_2], way_vertexes[index_1]
        
        return way_vertexes, way_edges, can_swap
    
    def calculate_length(self, way_edges) -> int:
        length = 0
        for edge in way_edges: length += edge["weight"]
        return length
    

class Individ:
    def __init__(self, graph: nx.DiGraph) -> None:
        self._graph = graph
        self._visited = dict.fromkeys(graph.nodes, False)
        self._way_node = list()
        self._way_long = 0
        self._way = list()
        
    @property
    def visited(self):
        return self._visited
    
    @property
    def way_node(self):
        return self._way_node
    
    @property
    def way_long(self):
        return self._way_long
    
    @property
    def way(self):
        return self._way
    
    def algoritm(self):
        lifo = q.LifoQueue()
        lifo.put(1)
        while not lifo.empty():
            min_weight_edge = {"from": None, "to": None, "weight": float('inf')}
            vertex = lifo.get()
            if self._visited[vertex]: continue
            else: self._visited[vertex] = True

            neighbors = []
            rand_coefficient = []
            for neighbor in self._graph.neighbors(vertex):
                if not self._visited[neighbor]:
                    neighbors.append((neighbor, self._graph[vertex][neighbor]["weight"]))
                    rand_coefficient.append(FUNCTION(neighbors[-1][1]))
                    
            if len(neighbors) > 0:
                new_vertex = random.choices(neighbors, rand_coefficient)[0]
                min_weight_edge = {"from": vertex, "to": new_vertex[0], "weight": new_vertex[1]}
                self._way_long += new_vertex[1]
                
            if min_weight_edge["weight"] == float('inf'):

                if all([self._visited[x] for x in self._graph.nodes]) and self._graph.has_edge(vertex, 1):
                    self._way.append({"from": vertex, "to": 1, "weight": self._graph[vertex][1]["weight"]})
                    self._way_long += self._graph[vertex][1]["weight"]

                else: self._way_long = 10**6
                
                return

            self._way.append(min_weight_edge)
            lifo.put(self._way[-1]["to"])
    
        self._way_long = 10**6   