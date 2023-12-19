import pytest
import sys
import requests
import numpy as np
import yaml
import csv
from io import StringIO
from unittest.mock import patch
sys.path.insert(0, f"C:/Users/sacke/ResearchSoftwareEngineering/working_group_4/repository/londontube")
from Network import Network
from query import query_disruptions, query_line_connections, query_station_information, query_station_num, parse_station_data

with open("tests/fixture.yaml", "r") as yamlfile:
    fixture = yaml.safe_load(yamlfile)
    

@pytest.mark.parametrize("data", [fixture[0]])
def test_adding_networks(data):
    properties = list(data.values())[0]
    Network1 = Network(4, *properties["Matrix1"])
    Network2 = Network(4, *properties["Matrix2"])
    expected = Network(4, *properties["expectedMatrix"])
    result = Network1 + Network2
    assert result.n_nodes == expected.n_nodes
    assert np.array_equal(result.adjacency_matrix, expected.adjacency_matrix)

@pytest.mark.parametrize("data", [fixture[1]])
def test_incompatible_networks(data):
    properties = list(data.values())[0]
    Network1 = Network(4, *properties["Matrix1"])
    Network2 = Network(5, *properties["Matrix2"])
    with pytest.raises(ValueError, match="The two objects have different numbers of nodes"):
        result = Network1 + Network2

@pytest.mark.parametrize("data", [fixture[2]])
def test_distant_neighbours(data):
    properties = list(data.values())[0]
    expected = properties["expected"]
    result = Network.distant_neighbours(1, 4, *properties["Matrix1"])
    assert result == expected

@pytest.mark.parametrize("data", [fixture[3]])
def test_dijstra_paths(data):
    properties = list(data.values())[0]
    expected = tuple(properties["expected"])
    result = Network.dijkstra(0, 4, *properties["Matrix1"])
    print(type(result))
    assert expected == result

@pytest.mark.parametrize("data", [fixture[4]])
def test_no_possible_paths(data):
    properties = list(data.values())[0]
    expected = None
    result = Network.dijkstra(0, 2, *properties["Matrix1"])
    assert expected == result

@pytest.mark.parametrize("data", [fixture[5]])
def test_query_line_connections(data):
    with patch.object(requests, "get") as mock_get:
        properties = list(data.values())[0]
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = properties["content"]
        result = query_line_connections(2)
        adjacency = np.zeros((296,296))
        reader = csv.reader(StringIO(properties["content"]))
        for row in reader:
            station1_index, station2_index, travel_time = map(int, row)           
            adjacency[station1_index, station2_index] = travel_time
            adjacency[station2_index, station1_index] = travel_time
        expected = Network(len(adjacency), adjacency)
        assert np.array_equal(expected.adjacency_matrix, result.adjacency_matrix)
        assert expected.n_nodes == result.n_nodes


@pytest.mark.parametrize("data", [fixture[6]])
def test_parse_station_data(data):
    with patch.object(requests, "get") as mock_get:
        properties = list(data.values())[0]
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = properties["content"]
        csv_data = properties["content"].strip()
        result = parse_station_data(csv_data)
        expected = properties["expected"]
        assert result == expected

    
@pytest.mark.parametrize("data", [fixture[6]])
def test_query_station_information(data):
    with patch.object(requests, "get") as mock_get:
        properties = list(data.values())[0]
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = properties["content"]
        result = query_station_information(1)
        expected = properties["expected"]
        assert result == expected

# def test_requests():
#     with patch.object(requests, "get") as mock_get:
#         result = query_line_connections(2)
#         mock_get.return_value.status_code = 200
#         mock_get.assert_called_with("https://rse-with-python.arc.ucl.ac.uk/londontube-service/line/query?line_identifier=2")

