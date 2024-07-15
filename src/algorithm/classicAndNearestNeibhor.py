import networkx as nx
import queue as q
import random
import math

class Function:
    def __init__(self, func:str) -> None:
        self._function = func
        
    def new_function(self, func: str)->None:
        self._function = func
        
    def mean(self, t: float)->float:
        return eval(self._function)

class Algorithm:
    def __init__(self) -> None:
        self._graph = nx.DiGraph()
        self._func_T = Function('0.999*t')
        self._start_T = 10.0**(15)
        self._end_T = 10.0**(-15)
        self._func_F = random.sample
        self._func_E = self.calculate_length
        self._func_swap = Function('-t/10**10')
        
    def init_graph(self, vertex_num: int, edges: list[dict])->None:
        self._graph.add_nodes_from([(x+1) for x in range(vertex_num)])
        for edge in edges:
            self._graph.add_edge(edge["from"], edge["to"], weight=edge["weight"])
            
            
    def search_hamilton_cycle(self) -> list[dict]:
        edges_way = self.search_first_way()
        if len(edges_way) == 0: return edges_way
        vertexes_way = [edge["from"] for edge in edges_way]
        nearest_point = [0, 
                         vertexes_way[-1], 
                         vertexes_way[len(vertexes_way) // 4],
                         vertexes_way[len(vertexes_way) * 3 // 4],
                         vertexes_way[len(vertexes_way) // 2 + 1],
                         vertexes_way[len(vertexes_way) // 2 - 1]
                         ]
        
        nearestes_ways = []
        for point in nearest_point:
            may_nearest_way = self.nearest_method(point)
            if len(may_nearest_way) > 0:
                nearestes_ways.append(may_nearest_way)
        if len(nearestes_ways) > 0:
            min_nearest_way = min(nearestes_ways, key=lambda x: self._func_E(x))
        else: min_nearest_way = [{"from": 1,"to": 1,"weight": 10**6}]
        
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
                # if random.random() < math.exp(-(new_length - length)/current_T):
                if random.random() < math.exp(-(new_length - length + 1) / current_T):
                    vertexes_way = new_vertexes_way.copy()
                    edges_way = new_edges_way.copy()
            
            current_T = self._func_T.mean(current_T)

        # print(min_length, self._func_E(min_edges_way))
        return min(min_edges_way, min_nearest_way, key=lambda x: self._func_E(x))
    
    
    def search_first_way(self) -> list[dict]:
        lifo = q.LifoQueue()
        visited = dict.fromkeys(self._graph.nodes, False)
        visited[1] = True
        lifo.put((1, visited, []))
        
        while not lifo.empty():
            vertex, visited, way = lifo.get()
            way = list(way); visited = dict(visited)
            may_way = []
            
            for neighbor in self._graph.neighbors(vertex):
                if not visited[neighbor]:
                    visited[neighbor] = True
                    way.append({"from": vertex, "to": neighbor, "weight": self._graph[vertex][neighbor]["weight"]})
                    # lifo.put((neighbor, visited.copy(), way.copy()))
                    may_way.append((neighbor, visited.copy(), way.copy()))
                    visited[neighbor] = False
                    way.pop(-1)
            for edge in sorted(may_way, key= lambda x: self._func_E(x[2])):
                lifo.put(edge)
            
            if all([visited[x] for x in self._graph.nodes]) and self._graph.has_edge(vertex, 1):
                way.append({"from": vertex, "to": 1, "weight": self._graph[vertex][1]["weight"]})
                return way
            
        return []
    
    def nearest_method(self, first_vertex) ->list[dict]:
        # Поиск гамильтонова цикла с помощью алгоритма ближайшего соседа
        lifo = q.LifoQueue()  # LIFO очередь для хранения вершин
        lifo.put(1)  # Начинаем с вершины 1
        visited = dict.fromkeys(self._graph.nodes, False)  # Словарь для отслеживания посещенных вершин
        way = list()  # Список для хранения найденного пути
        
        while not lifo.empty():
            min_weight_edge = {"from": None, "to": None, "weight": float('inf')}  # Минимальное ребро из текущей вершины
            vertex = lifo.get()  # Получаем текущую вершину из очереди
            if visited[vertex]:  # Если вершина уже посещена, пропускаем ее
                continue
            else:
                visited[vertex] = True  # Помечаем вершину как посещенную
            
            for neighbor in self._graph.neighbors(vertex):  # Просматриваем соседей текущей вершины
                weight = self._graph[vertex][neighbor]["weight"]  # Получаем вес ребра до соседней вершины
                if weight < min_weight_edge["weight"] and not visited[neighbor]:  # Если вес меньше минимального и соседняя вершина не посещена
                    min_weight_edge = {"from": vertex, "to": neighbor, "weight": weight}  # Обновляем минимальное ребро
                    
            if min_weight_edge["weight"] == float('inf'):  # Если не найдено подходящего ребра
                if all([visited[x] for x in self._graph.nodes]) and self._graph.has_edge(vertex, 1):  # Если все вершины посещены и есть ребро к начальной вершине
                    way.append({"from": vertex, "to": 1, "weight": self._graph[vertex][1]["weight"]})  # Добавляем ребро к начальной вершине
                    return way  # Возвращаем найденный путь
                
                return []  # Возвращаем найденный путь
                    
            way.append(min_weight_edge)  # Добавляем минимальное ребро в путь
            lifo.put(way[-1]["to"])  # Помещаем следующую вершину в очередь
        
        return []  # Возвращаем путь (может быть неполным)

    
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