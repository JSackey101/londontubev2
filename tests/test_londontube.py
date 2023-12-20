import pytest
import requests
import numpy as np
import yaml
import csv
from io import StringIO
from unittest.mock import patch
from Network import Network
from query import query_disruptions, query_line_connections, query_station_information, query_station_num, parse_station_data, parse_disruptions_data


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

@pytest.mark.parametrize("data", [fixture[7]])
def test_query_station_num(data):
    with patch.object(requests, "get") as mock_get:
        properties = list(data.values())[0]
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = properties["content"]
        result = query_station_num("Warren Street")
        expected = properties["expected"]
        assert result == expected


@pytest.mark.parametrize("data", [fixture[8]])
def test_query_disruptions(data):
    with patch.object(requests, "get") as mock_get:
        properties = list(data.values())[0]
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = properties["content"]
        result = query_disruptions("2023-12-15")
        expected = properties["expected"]
        assert result == expected


@pytest.mark.parametrize("data", [fixture[8]])
def test_parse_distruptions_data(data):
    with patch.object(requests, "get") as mock_get:
        properties = list(data.values())[0]
        result = parse_disruptions_data(properties["content"])
        expected = properties["expected"]
        assert result == expected

@pytest.mark.parametrize("data", [(fixture[9]),(fixture[10]),(fixture[11]),(fixture[12]),
                                  (fixture[13]),(fixture[14]),(fixture[15]),(fixture[27]),
                                  (fixture[28]), (fixture[29])])
def test_query_value_error(data):
    with patch.object(requests, "get") as mock_get:
        properties = list(data.values())[0]
        mock_get.return_value.status_code = 201
        with pytest.raises(ValueError, match=properties["errormsg"]):
            exec(properties["execute"])

@pytest.mark.parametrize("data", [(fixture[16]),(fixture[17]),(fixture[18])])
def test_query_type_error(data):
    with patch.object(requests, "get") as mock_get:
        properties = list(data.values())[0]
        mock_get.return_value.status_code = 201
        with pytest.raises(TypeError, match=properties["errormsg"]):
            exec(properties["execute"])

@pytest.mark.parametrize("data", [(fixture[19]),(fixture[20]),(fixture[21]),(fixture[22])])
def test_connection_error(data):
    with patch.object(requests, "get") as mock_get:
        properties = list(data.values())[0]
        mock_get.return_value.status_code.return_value = 200
        mock_get.side_effect = requests.ConnectionError
        with pytest.raises(ConnectionError, match=properties["errormsg"]):
            exec(properties["execute"])

@pytest.mark.parametrize("data", [(fixture[23]),(fixture[24]),(fixture[25]),(fixture[26])])
def test_requests(data):
    with patch.object(requests, "get") as mock_get:
        properties = list(data.values())[0]
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = properties["content"]
        result = exec(properties["execute"])
        mock_get.assert_called_with(properties["call"])
