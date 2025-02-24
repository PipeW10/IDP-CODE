from pathfinding.core.grid import Grid 
from pathfinding.finder.a_star import AStarFinder 
from pathfinding.core.diagonal_movement import DiagonalMovement 

matrix = [
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
print(path)
