import numpy as np
import argparse
from datetime import datetime
import matplotlib.pyplot as plt

class Network:
    """
    Create a class called Network to show the number of nodes, and the adjacency matrix.
    """
    def __init__(self, n_nodes, adjacency_matrix):
        self.n_nodes = n_nodes
        self.adjacency_matrix = adjacency_matrix   
    
    def __add__(self, Network2):
        """
        Make the Network class be able to operate with + on other Network objects.
        """
        if self.n_nodes != Network2.n_nodes:
            raise ValueError("The two objects have different numbers of nodes")

        new_adjacency_matrix = np.empty((len(self.adjacency_matrix), len(self.adjacency_matrix[0])))
        
        for i in range(len(self.adjacency_matrix)):
            for j in range(len(self.adjacency_matrix[i])):
                if self.adjacency_matrix[i][j] == 0 and Network2.adjacency_matrix[i][j] == 0:
                    new_adjacency_matrix[i][j] = 0
                elif self.adjacency_matrix[i][j] == 0 or Network2.adjacency_matrix[i][j] == 0:
                    new_adjacency_matrix[i][j] = max(self.adjacency_matrix[i][j], Network2.adjacency_matrix[i][j])
                else:
                    new_adjacency_matrix[i][j] = min(self.adjacency_matrix[i][j], Network2.adjacency_matrix[i][j])
        return Network(self.n_nodes, new_adjacency_matrix)

    def distant_neighbours(n, v, adjacency_matrix): 
        """
        Compute the 𝑛-distant neighbours of a particular node.
        """
        matrix = np.array(adjacency_matrix, dtype=int)
        neighbours = [v]
        index_neighbours = np.full((1,len(matrix[0])), False).flatten()
        for i in range(n):
            for index in neighbours:
                row = matrix[index]
                for j in range(len(row)):
                    if (row[j] > 0) and (j not in list(np.where(index_neighbours == True)[0])):
                        index_neighbours[j] = True
            neighbours += list(set(np.where(index_neighbours == True)[0]) - set(neighbours))
        while v in neighbours:
            neighbours.remove(v)
        return neighbours
    
    def dijkstra(start_node, dest_node, adjacency_matrix):
        """
        Compute the path across the network with the lowest cost between a start and destination node, 
        using Dijkstra’s algorithm.
        """
        tenative_cost = list(np.full((1,len(adjacency_matrix[0])), np.inf).flatten())
        tenative_cost[start_node] = 0
        previous_node = [None] * len((adjacency_matrix[0]))
        current_node = start_node
        visited_nodes = []
        unvisited_nodes = list(np.arange(0, len(adjacency_matrix[0])))
        
        tenative_cost[start_node] = 0
        for node in range(len(previous_node)):
            previous_node[node] = start_node
        
        dest_not_reached = True
        while dest_not_reached:
            nodes = Network.distant_neighbours(1, current_node, adjacency_matrix)
            for node in nodes:
                proposed_cost =  adjacency_matrix[current_node][node] + tenative_cost[current_node]
                if proposed_cost < tenative_cost[node]:
                    tenative_cost[node] = proposed_cost
                    previous_node[node] = current_node
        
            visited_nodes.append(current_node)
            unvisited_nodes.remove(current_node)

            if dest_node in visited_nodes:
                dest_not_reached = False
            elif min([tenative_cost[i] for i in unvisited_nodes]) == np.inf:
                print("No possible paths.")
                return None
            else:
                current_node = unvisited_nodes[([tenative_cost[i] for i in unvisited_nodes]).index(min(([tenative_cost[i] for i in unvisited_nodes])))]
        path_list = []
        current_node = dest_node
        path_not_reconstructed = True
        while path_not_reconstructed:
            path_list.append(current_node)
            if previous_node[current_node] == start_node:
                path_list.append(start_node)
                path_list.reverse() 
                path_not_reconstructed = False
            else:
                current_node = previous_node[current_node]
        
        return path_list,tenative_cost[dest_node]
 


