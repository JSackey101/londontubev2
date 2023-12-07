import numpy as np

class Network:
    def __init__(self, n_nodes, adjacency_matrix):
        self.n_nodes = n_nodes
        self.adjacency_matrix = adjacency_matrix    
    
    def __add__(self, Network2):
        if self.n_nodes != Network2.n_nodes:
            raise ValueError("The two objects have different numbers of nodes")
        new_adjacency_matrix = np.empty((4,4))
        for i in range(len(self.adjacency_matrix)):
            for j in range(len(self.adjacency_matrix[i])):
                if self.adjacency_matrix[i][j] == 0 and Network2.adjacency_matrix[i][j] == 0:
                    new_adjacency_matrix[i][j] = 0
                elif self.adjacency_matrix[i][j] == 0 or Network2.adjacency_matrix[i][j] == 0:
                    new_adjacency_matrix[i][j] = max(self.adjacency_matrix[i][j], Network2.adjacency_matrix[i][j])
                else:
                    new_adjacency_matrix[i][j] = min(self.adjacency_matrix[i][j], Network2.adjacency_matrix[i][j])
        return Network(self.n_nodes, new_adjacency_matrix)

