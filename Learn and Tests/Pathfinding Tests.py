from pathfinding.core.grid import Grid 
from pathfinding.finder.a_star import AStarFinder 
from pathfinding.core.diagonal_movement import DiagonalMovement 
from heapq import heapify, heappop, heappush

"""matrix = [
    [1,1,1,1,1,1],
    [1,1,0,1,1,1],
    [1,1,1,1,1,1]
]

#Grid Creation
grid  = Grid(matrix = matrix)

#2. create start and end node
start = grid.node(0,0)
end = grid.node(5,2)

#3. create a finder with a movement style
finder = AStarFinder(diagonal_movement = DiagonalMovement.always)

#4. Use finder to find path 
path, runs = finder.find_path(start,end,grid)

#Print result
print(path)"""

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
                    
        
adjacency_map = {
    "locA" : {"f" : norm_cost},
    "locB" : {"j" : norm_cost},
    "locC" : {"q" : norm_cost},
    "locD" : {"o" : norm_cost},
    "e" : {"f" : norm_cost, "l" : norm_cost, "dep1" : norm_cost},
    "f" : {"locA" : norm_cost, "e" : norm_cost, "g" : norm_cost},
    "g" : {"f" : norm_cost, "h" : norm_cost, "start" : norm_cost},
    "h" : {"g" : norm_cost, "i" : norm_cost, "dep2" : norm_cost},
    "i" : {"h" : norm_cost, "j" : norm_cost, "p" : norm_cost},   
    "j" : {"locB" : norm_cost, "i" : norm_cost, "k" : norm_cost},
    "k" : {"j" : norm_cost, "l" : norm_cost, "q" : norm_cost},
    "l" : {"e" : norm_cost, "k" : norm_cost, "m" : norm_cost},
    "m" : {"l" : norm_cost, "n" : norm_cost}, 
    "n" : {"m" : norm_cost, "o" : norm_cost / 2, "q" : norm_cost},
    "o" : {"locD" : norm_cost, "n" : norm_cost / 2, "p" : norm_cost / 2},
    "p" : {"i" : norm_cost, "o" : norm_cost / 2}, 
    "q" : {"locC" : norm_cost, "k" : norm_cost, "n" : norm_cost},
    "start" : {"g" : norm_cost},
    "dep2" : {"e" : norm_cost},
    "dep1" : {"h" : norm_cost}}

map = Graph(graph = adjacency_map)

start_distances, start_predecessors = map.shortest_distance("start")

print (map.shortest_path("start", "locD"), start_distances["locD"])