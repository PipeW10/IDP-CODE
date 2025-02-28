class Navigator:
    
    def __init__ (self):
        self.dirc_paths = {'locA': {'dep1': [3, 4, 3], 'dep2': [3, 2, 2, 3]}, 
                      'locB': {'dep1': [1, 4, 4, 3, 3], 'dep2': [1, 2, 3, 3]}, 
                      'locC': {'dep1': [2, 3, 4, 3, 3], 'dep2': [2, 3, 2, 2, 3, 3]}, 
                      'locD': {'dep1': [1, 4, 4, 3, 3, 3], 'dep2': [1, 2, 3, 3, 3]}, 
                      'start': {'locA': [1, 4, 1]}, 
                      'dep2': {'locB': [1, 1, 2, 2, 3], 'locC': [1, 1, 2, 1, 4], 'locD': [1, 1, 2, 1, 1, 2, 3], 'start': [1, 2, 2, 3]}, 
                      'dep1': {'locB': [1, 1, 2, 2, 3], 'locC': [1, 1, 2, 1, 4], 'locD': [1, 1, 2, 1, 1, 2, 3], 'start': [1, 2, 2, 3]}}
        self.node_paths = {'locA': {'dep1': ['locA', 'f', 'e', 'dep1'], 'dep2': ['locA', 'f', 'g', 'h', 'dep2']}, 
                      'locB': {'dep1': ['locB', 'j', 'k', 'l', 'e', 'dep1'], 'dep2': ['locB', 'j', 'i', 'h', 'dep2']}, 
                      'locC': {'dep1': ['locC', 'q', 'k', 'l', 'e', 'dep1'], 'dep2': ['locC', 'q', 'k', 'j', 'i', 'h', 'dep2']}, 
                      'locD': {'dep1': ['locD', 'o', 'n', 'm', 'l', 'e', 'dep1'], 'dep2': ['locD', 'o', 'p', 'i', 'h', 'dep2']}, 
                      'start': {'locA': ['start', 'g', 'f', 'locA']}, 
                      'dep2': {'locB': ['dep2', 'e', 'l', 'k', 'j', 'locB'], 'locC': ['dep2', 'e', 'l', 'k', 'q', 'locC'], 'locD': ['dep2', 'e', 'l', 'k', 'q', 'n', 'o', 'locD'], 'start': ['dep2', 'e', 'f', 'g', 'start']}, 
                      'dep1': {'locB': ['dep2', 'e', 'l', 'k', 'j', 'locB'], 'locC': ['dep2', 'e', 'l', 'k', 'q', 'locC'], 'locD': ['dep2', 'e', 'l', 'k', 'q', 'n', 'o', 'locD'], 'start': ['dep2', 'e', 'f', 'g', 'start']}}
        
    def return_dircs(self, start, end):
        return self.dirc_paths[start][end]
    
    def return_nodes(self, start, end):
        return self.node_paths[start][end]