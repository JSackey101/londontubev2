import requests
from datetime import date
import csv
from io import StringIO
import numpy as np
import time
from distant_neighbours import distant_neighbours as distant_neighbours_provided
import matplotlib.pyplot as plt
from Network import Network


def query_line_connections(line_identifier):
    # Set the default line_identifier to 0 (Bakerloo) if not specified
    line_identifier = line_identifier or "0"

    # Make a request to the web service to get line connections
    url = f"https://rse-with-python.arc.ucl.ac.uk/londontube-service/line/query?line_identifier={line_identifier}"
    response = requests.get(url)

    if response.status_code == 200:
        # Parse CSV data from the response
        csv_data = StringIO(response.text)
        reader = csv.reader(csv_data)

        # Process each row in the CSV data
        connections = []
        for row in reader:
            station1_index, station2_index, travel_time = map(int, row)
            connections.append((station1_index, station2_index, travel_time))

        return connections
    else:
        print(f"Error: Unable to fetch line connections for {line_identifier}.")
        return []


def query_station_information(ids):
    # Set the default ids to "0" if not specified
    ids = ids or "0"

    # If a single id is provided as a string, convert it to a list
    if isinstance(ids, str):
        ids = [ids]

    # Make a request to the web service to get station information
    url = f"https://rse-with-python.arc.ucl.ac.uk/londontube-service/stations/query?id={','.join(ids)}"
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the CSV response
        csv_data = response.text.strip()
        station_info_matrix = parse_station_data(csv_data)

        # Print the station information matrix
        return station_info_matrix
    else:
        print(f"Error: Unable to fetch station information for {ids}.")
        return []

def parse_station_data(csv_data):
    # Parse the CSV data and return station information as a matrix-like structure
    station_info_matrix = []

    # Use StringIO to convert the CSV data string to a file-like object
    csv_file = StringIO(csv_data)

    # Use the CSV module to read the file-like object
    csv_reader = csv.DictReader(csv_file)

    for row in csv_reader:
        station_info = [
            int(row["station index"]),
            row["station name"],
            float(row["latitude"]),
            float(row["longitude"])
        ]
        station_info_matrix.append(station_info)

    # Sort station information by station index
    station_info_matrix.sort(key=lambda x: x[0])

    return station_info_matrix



def query_disruptions(date_str=None):
    # Set the default date to the present day if not provided
    if date_str is None:
        date_str = str(date.today())
    else:
        # Validate and set the provided date within the valid range
        try:
            provided_date = date.fromisoformat(date_str)
            valid_start_date = date(2023, 1, 1)
            valid_end_date = date(2024, 12, 31)

            if not valid_start_date <= provided_date <= valid_end_date:
                print("Warning: Provided date outside the valid range. Using the present day.")
                date_str = str(date.today())
        except ValueError:
            print("Error: Invalid date format. Using the present day.")
            date_str = str(date.today())

    # Make a request to the web service to get disruption information
    url = f"https://rse-with-python.arc.ucl.ac.uk/londontube-service/disruptions/query?date={date_str}"
    response = requests.get(url)

    if response.status_code == 200:
        disruptions_data = response.json()
        disruptions_matrix = parse_disruptions_data(disruptions_data)

        # Print the disruptions matrix
        print_matrix(disruptions_matrix)
    else:
        print(f"Error: Unable to fetch disruption information for {date_str}.")


def parse_disruptions_data(disruptions_data):
    # Parse the disruption data and return it as a matrix-like structure
    disruptions_matrix = []

    for event in disruptions_data:
        disruption = [
            event.get("line"),
            event.get("stations", []),
            event.get("delay", 0)
        ]
        disruptions_matrix.append(disruption)

    return disruptions_matrix


def print_matrix(matrix):
    # Print the matrix in a readable format
    for row in matrix:
        print(row)


station_list = []
for i in range(12):
    connections_matrix = query_line_connections(i)
    for information in connections_matrix:
        station_list.append(information)

weight_matrix = np.zeros((296, 296))
for stations in station_list:
    j, i, k = stations
    weight_matrix[i][j] = k
    weight_matrix[j][i] = k

# List of n_values
n_values = [1, 2, 3, 4, 5, 7, 8, 10, 12, 14, 17, 20, 25, 29, 35, 42, 51, 61, 73, 87, 104, 125, 149, 179, 214, 256]

# List of station_id values
v_values = [10, 24, 56, 73, 83, 94, 144, 168, 265]

# Lists to store average times
average_time_network = []
average_time_provided = []

# Iterate through n_values and v_values
for n_value in n_values:
    # Lists to store individual times for each method
    times_network = []
    times_provided = []

    for v_value in v_values:
        # Measure execution time for Network.distant_neighbours
        start_time_network = time.time()
        Network.distant_neighbours(n_value, v_value, weight_matrix)
        elapsed_time_network = time.time() - start_time_network
        times_network.append(elapsed_time_network)

        # Measure execution time for the provided method
        start_time_provided = time.time()
        result = distant_neighbours_provided(n_value, v_value, weight_matrix)
        elapsed_time_provided = time.time() - start_time_provided
        times_provided.append(elapsed_time_provided)

    # Calculate average times for each method
    average_time_network.append(sum(times_network) / len(times_network))
    average_time_provided.append(sum(times_provided) / len(times_provided))

# Plotting with log axes
plt.semilogy(n_values, average_time_network, label='Network.distant_neighbours')
plt.semilogy(n_values, average_time_provided, label='Provided method')
plt.xlabel('n')
plt.ylabel('Average Time (secs)')
plt.legend()
plt.title('Average Execution Time vs. n')
plt.show()