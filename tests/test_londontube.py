import pytest
import sys
import numpy as np
sys.path.insert(0, f"C:/Users/sacke/ResearchSoftwareEngineering/working_group_4/repository/londontube")
from Network import Network



def test_adding_n_nodes():
    Matrix1 = [
        [0, 1, 0, 0],
        [1, 0, 2, 0],
        [0, 2, 0, 0],
        [0, 0, 0, 0]
    ]
    Matrix2 = [
        [0, 0, 0, 3],
        [0, 0, 0, 1],
        [0, 0, 0, 0],
        [3, 1, 0, 0]
    ]
    Network1 = Network(4, Matrix1)
    Network2 = Network(4, Matrix2)
    expected = Network(4, [
        [0, 1, 0, 3],
        [1, 0, 2, 1],
        [0, 2, 0, 0],
        [3, 1, 0, 0]
    ])
    result = Network1 + Network2
    assert result.n_nodes == expected.n_nodes

def test_adding_adjacency_matrix():
    Matrix1 = [
        [0, 1, 0, 0],
        [1, 0, 2, 0],
        [0, 2, 0, 0],
        [0, 0, 0, 0]
    ]
    Matrix2 = [
        [0, 0, 0, 3],
        [0, 0, 0, 1],
        [0, 0, 0, 0],
        [3, 1, 0, 0]
    ]
    Network1 = Network(4, Matrix1)
    Network2 = Network(4, Matrix2)
    expected = Network(4, [
        [0, 1, 0, 3],
        [1, 0, 2, 1],
        [0, 2, 0, 0],
        [3, 1, 0, 0]
    ])
    result = Network1 + Network2
    assert np.array_equal(result.adjacency_matrix, expected.adjacency_matrix)

def test_incompatible_networks():
    Matrix1 = [
        [0, 1, 0, 0],
        [1, 0, 2, 0],
        [0, 2, 0, 0],
        [0, 0, 0, 0]
    ]
    Matrix2 = [
        [0, 0, 0, 3, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0],
        [3, 1, 0, 0, 0],
        [1, 0, 0, 1, 2]
    ]
    Network1 = Network(4, Matrix1)
    Network2 = Network(5, Matrix2)
    with pytest.raises(ValueError, match="The two objects have different numbers of nodes"):
        result = Network1 + Network2
