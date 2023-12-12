import time


# The distant_neighbours function that we are providing finds the INDEX of the n-distant neighbours to the vertex with index v, given the adjacency matrix.
# The adjacency matrix must be indexable using [i][j] notation.
def distant_neighbours(n, v, adjacency_matrix):
    neighbours = [v]
    for i in range(n):
        new_neighbours = []
        for index in neighbours:
            row = adjacency_matrix[index]
            for j in range(len(row)):
                if (row[j] > 0) and (j not in neighbours) and (j not in new_neighbours):
                    new_neighbours.append(j)
        neighbours += new_neighbours
    while v in neighbours:
        neighbours.remove(v)
    return neighbours


if __name__ == "__main__":
    # The rest of this script will execute the function above on the example network from the assignment.

    # This is the adjacency matrix of the example network from the assignment:
    A = [
        [0, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 1, 0, 0, 1, 1, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 1, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 1, 1, 0],
    ]

    # Each element of this list is a tuple,
    # (n, v, expected),
    # where n, and v are the inputs to distant_neighbours,
    # and expected is the list of n-distant-neighbours that should be returned by the function.
    n_v_expected = [
        (1, 0, [1]),
        (2, 0, [1, 4]),
        (3, 0, [1, 4, 2, 5, 6]),
        (1, 4, [1, 2, 5, 6]),
        (2, 4, [0, 1, 2, 3, 5, 6, 7, 8]),
        (4, 4, [0, 1, 2, 3, 5, 6, 7, 8]),
    ]

    # Loops over each example input and displays the output of the function above, and the expected output underneath
    for triplet in n_v_expected:
        n = triplet[0]
        v = triplet[1]
        expected_neighbours = triplet[2]
        print(f"Computing {n}-distant neighbours of node {v}")

        slow_start = time.time()
        got_result = distant_neighbours(n, v, A)
        slow_end = time.time()
        got_result = sorted(got_result)
        print(
            f"\tGot (from fn): {got_result} \t| Time elapsed: {slow_end - slow_start}s"
        )

        print(f"\tExpected     : {sorted(expected_neighbours)}")




