from pathfinding.core.grid import Grid 
from pathfinding.finder.a_star import AStarFinder 
from pathfinding.core.diagonal_movement import DiagonalMovement 
from heapq import heapify, heappop, heappush

#Graph of Map with costings

norm_cost = 1

class Graph:
    def __init__ (self, graph: dict = {}):
        self.graph = graph
        
    def add_edge (self, node1, node2, cost):
        if node1 not in self.graph:
            self.graph[node1] = {}
        self.graph[node1][node2] = cost
    
    def shortest_distance (self, source: str):
        #Initialize all nodes with inf value
        distances = {node: float("inf") for node in self.graph}
        distances[source] = 0
        
        #Initialize Priority Queue
        pq = [(0, source)]
        heapify(pq)
        
        #Create a set to hold visited nodes
        visited = set()
        
        #Using djikstra"s
        while pq: #While the queue is not empty
            current_distance, current_node = heappop(pq) #Get shortest connected node
            
            if current_node in visited:
                continue #skip visited nodes
            visited.add(current_node) #Otherwise add current_node
        
            for neighbor, weight in self.graph[current_node].items():
            # Calculate the distance from current_node to the neighbor
                tentative_distance = current_distance + weight
                if tentative_distance < distances[neighbor]:
                    distances[neighbor] = tentative_distance
                    heappush(pq, (tentative_distance, neighbor))

            predecessors = {node: None for node in self.graph}

            for node, distance in distances.items():
                for neighbor, weight in self.graph[node].items():
                    if distances[neighbor] == distance + weight:
                        predecessors[neighbor] = node

        return distances, predecessors
    
    def shortest_path(self, source: str, target: str):
        # Generate the predecessors dict
        _, predecessors = self.shortest_distance(source)

        path = []
        current_node = target

        # Backtrack from the target node using predecessors
        while current_node:
            path.append(current_node)
            current_node = predecessors[current_node]

        # Reverse the path and return it
        path.reverse()

        return path
    
    def path_direction (self, path, dirc_map):
        directions = []
        
        
        for i in range(len(path) - 1):
            directions.append(dirc_map[path[i]][path[i+1]])
        return directions 
        
                    
        
adjacency_map = {
    "locA" : {"f" : norm_cost},
    "locB" : {"j" : norm_cost},
    "locC" : {"q" : norm_cost},
    "locD" : {"o" : norm_cost},
    "e" : {"f" : norm_cost / 2, "l" : norm_cost, "dep1" : norm_cost},
    "f" : {"locA" : norm_cost, "e" : norm_cost / 2, "g" : norm_cost / 2},
    "g" : {"f" : norm_cost / 2, "h" : norm_cost, "start" : norm_cost},
    "h" : {"g" : norm_cost, "i" : norm_cost, "dep2" : norm_cost},
    "i" : {"h" : norm_cost, "j" : norm_cost / 2, "p" : norm_cost},   
    "j" : {"locB" : norm_cost, "i" : norm_cost / 2, "k" : norm_cost / 2},
    "k" : {"j" : norm_cost / 2, "l" : norm_cost, "q" : norm_cost / 2},
    "l" : {"e" : norm_cost, "k" : norm_cost, "m" : norm_cost},
    "m" : {"l" : norm_cost, "n" : norm_cost}, 
    "n" : {"m" : norm_cost, "o" : norm_cost / 2, "q" : norm_cost / 2},
    "o" : {"locD" : norm_cost, "n" : norm_cost / 2, "p" : norm_cost / 2},
    "p" : {"i" : norm_cost, "o" : norm_cost / 2}, 
    "q" : {"locC" : norm_cost, "k" : norm_cost / 2, "n" : norm_cost / 2},
    "start" : {"g" : norm_cost},
    "dep2" : {"e" : norm_cost},
    "dep1" : {"h" : norm_cost}}

# N = 1 E = 2 S = 3 W = 4

direction_map = {
    "locA" : {"f" : 3},
    "locB" : {"j" : 1},
    "locC" : {"q" : 2},
    "locD" : {"o" : 1},
    "e" : {"f" : 2, "l" : 1, "dep1" : 3},
    "f" : {"locA" : 1, "e" : 4, "g" : 2},
    "g" : {"f" : 4, "h" : 2, "start" : 3},
    "h" : {"g" : 4, "i" : 1, "dep2" : 3},
    "i" : {"h" : 3, "j" : 4, "p" : 1},   
    "j" : {"locB" : 3, "i" : 2, "k" : 4},
    "k" : {"j" : 2, "l" : 4, "q" : 1},
    "l" : {"e" : 3, "k" : 2, "m" : 1},
    "m" : {"l" : 3, "n" : 2}, 
    "n" : {"m" : 4, "o" : 2, "q" : 3},
    "o" : {"locD" : 3, "n" : 4, "p" : 2},
    "p" : {"i" : 3, "o" : 4}, 
    "q" : {"locC" : 4, "k" : 3, "n" : 1},
    "start" : {"g" : 1},
    "dep2" : {"e" : 1},
    "dep1" : {"h" : 1}}

map = Graph(graph = adjacency_map)

start_distances, start_predecessors = map.shortest_distance("start")

#print (map.shortest_path("locD", "locC"), start_distances["locA"])

#print (map.path_direction(path = map.shortest_path("locD", "locC"), dirc_map = direction_map))

dirc_paths = {
    "locA" : {"dep1" : map.path_direction(path = map.shortest_path("locA", "dep1"), dirc_map = direction_map), "dep2" : map.path_direction(path = map.shortest_path("locA", "dep2"), dirc_map = direction_map)},
    "locB" : {"dep1" : map.path_direction(path = map.shortest_path("locB", "dep1"), dirc_map = direction_map), "dep2" : map.path_direction(path = map.shortest_path("locB", "dep2"), dirc_map = direction_map)},
    "locC" : {"dep1" : map.path_direction(path = map.shortest_path("locC", "dep1"), dirc_map = direction_map), "dep2" : map.path_direction(path = map.shortest_path("locC", "dep2"), dirc_map = direction_map)},
    "locD" : {"dep1" : map.path_direction(path = map.shortest_path("locD", "dep1"), dirc_map = direction_map), "dep2" : map.path_direction(path = map.shortest_path("locD", "dep2"), dirc_map = direction_map)},
    "start" : {"locA" : map.path_direction(path = map.shortest_path("start", "locA"), dirc_map = direction_map)},
    "dep2" : {"locB" : map.path_direction(path = map.shortest_path("dep2", "locB"), dirc_map = direction_map), "locC" : map.path_direction(path = map.shortest_path("dep2", "locC"), dirc_map = direction_map), "locD" : map.path_direction(path = map.shortest_path("dep2", "locD"), dirc_map = direction_map), "start": map.path_direction(path = map.shortest_path("dep2", "start"), dirc_map = direction_map)},
    "dep1" : {"locB" : map.path_direction(path = map.shortest_path("dep2", "locB"), dirc_map = direction_map), "locC" : map.path_direction(path = map.shortest_path("dep2", "locC"), dirc_map = direction_map), "locD" : map.path_direction(path = map.shortest_path("dep2", "locD"), dirc_map = direction_map), "start": map.path_direction(path = map.shortest_path("dep2", "start"), dirc_map = direction_map)}
    }

node_paths = {
    "locA" : {"dep1" : map.shortest_path("locA", "dep1"), "dep2" : map.shortest_path("locA", "dep2")},
    "locB" : {"dep1" : map.shortest_path("locB", "dep1"), "dep2" : map.shortest_path("locB", "dep2")},
    "locC" : {"dep1" : map.shortest_path("locC", "dep1"), "dep2" : map.shortest_path("locC", "dep2")},
    "locD" : {"dep1" : map.shortest_path("locD", "dep1"), "dep2" : map.shortest_path("locD", "dep2")},
    "start" : {"locA" : map.shortest_path("start", "locA")},
    "dep2" : {"locB" : map.shortest_path("dep2", "locB"), "locC" :map.shortest_path("dep2", "locC"), "locD" : map.shortest_path("dep2", "locD"), "start": map.shortest_path("dep2", "start")},
    "dep1" : {"locB" : map.shortest_path("dep2", "locB"), "locC" : map.shortest_path("dep2", "locC"), "locD" : map.shortest_path("dep2", "locD"), "start": map.shortest_path("dep2", "start")}
    }

print (node_paths)