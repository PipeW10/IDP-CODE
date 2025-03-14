#Class with the map coded in 
class Navigator:
    
    def __init__ (self):
        #Directional paths off all needed paths based on cardinal directions N = 1 E = 2 S = 3 W = 4
        self.dirc_paths = {'locA': {'dep1': [3, 2, 2, 3], 'dep2': [3, 4, 3]}, 
                           'locB': {'dep1': [1, 2, 3, 3], 'dep2': [1, 4, 4, 3, 3]}, 
                           'locC': {'dep1': [2, 3, 2, 2, 3, 3], 'dep2': [2, 3, 4, 3, 3]}, 
                           'locD': {'dep1': [1, 2, 3, 3, 3], 'dep2': [1, 4, 4, 3, 3, 3]}, 
                           'start': {'locA': [1, 4, 1]}, 
                           'dep2': {'locB': [1, 1, 2, 2, 3], 'locC': [1, 1, 2, 1, 4], 'locD': [1, 1, 2, 1, 1, 2, 3], 'start': [1, 2, 2, 3]}, 
                           'dep1': {'locB': [1, 1, 4, 3], 'locC': [1, 1, 4, 4, 1, 4], 'locD': [1, 1, 1, 4, 3], 'start': [1, 4, 3]}}
        #All needed paths with the node names for tracking purposes
        self.node_paths = {'locA': {'dep1': ['locA', 'f', 'g', 'h', 'dep1'], 'dep2': ['locA', 'f', 'e', 'dep2']}, 
                           'locB': {'dep1': ['locB', 'j', 'i', 'h', 'dep1'], 'dep2': ['locB', 'j', 'k', 'l', 'e', 'dep2']}, 
                           'locC': {'dep1': ['locC', 'q', 'k', 'j', 'i', 'h', 'dep1'], 'dep2': ['locC', 'q', 'k', 'l', 'e', 'dep2']}, 
                           'locD': {'dep1': ['locD', 'o', 'p', 'i', 'h', 'dep1'], 'dep2': ['locD', 'o', 'n', 'm', 'l', 'e', 'dep2']}, 
                           'start': {'locA': ['start', 'g', 'f', 'locA']}, 
                           'dep2': {'locB': ['dep2', 'e', 'l', 'k', 'j', 'locB'], 'locC': ['dep2', 'e', 'l', 'k', 'q', 'locC'], 'locD': ['dep2', 'e', 'l', 'k', 'q', 'n', 'o', 'locD'], 'start': ['dep2', 'e', 'f', 'g', 'start']}, 
                           'dep1': {'locB': ['dep1', 'h', 'i', 'j', 'locB'], 'locC': ['dep1', 'h', 'i', 'j', 'k', 'q', 'locC'], 'locD': ['dep1', 'h', 'i', 'p', 'o', 'locD'], 'start': ['dep1', 'h', 'g', 'start']}}
        
    def return_dircs(self, start, end):
        #Returns the needed directional path based on the start and end nodes given
        return self.dirc_paths[start][end]
    
    def return_nodes(self, start, end):
        #Returns the needed node path based on the start and end nodes given
        return self.node_paths[start][end]