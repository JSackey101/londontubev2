import requests
from datetime import date
import csv
from io import StringIO
import numpy as np
from Network import Network
import time
import matplotlib.pyplot as plt
from distant_neighbours import distant_neighbours as distant_neighbours_provided

def query_line_connections(line_identifier):
    """This function takes the line identifier, quering the web service for information
    about the connectivity of a particular line, and returns a Network object
    that represents that line.
    Arg:
        line_identifier (int): The ID for a particular line in London tube network
    Return:
        line_network (Network): A network object of the line, i.e. a sub-network of London tube
    """

    # Make a request to the web service to get line connections
    url = f"https://rse-with-python.arc.ucl.ac.uk/londontube-service/line/query?line_identifier={line_identifier}"
    response = requests.get(url)

    # Init a adjacency matrix with 296x296 (296 stations in London tube network)
    adjacency = np.zeros((296, 296))

    if response.status_code == 200:
        # Parse CSV data from the response
        csv_data = StringIO(response.text)
        reader = csv.reader(csv_data)

        # Process each row in the CSV data
        for row in reader:
            station1_index, station2_index, travel_time = map(int, row)
            # Fill the matrix by using station index
            adjacency[station1_index, station2_index] = travel_time
            adjacency[station2_index, station1_index] = travel_time

        # Create a Network object for the line
        line_network = Network(len(adjacency), adjacency)
        return line_network
    else:
        print(f"Error: Unable to fetch line connections for {line_identifier}.")
        return None


def query_station_information(ids):
    """This function takes the station ID and query the web service for station information
    Arg:
        ids (int, str): The ID for station/stations in London tube network. eg. 1 (int); "all" (str); "1, 3, 7" (str)
    Return:
        station_info_matrix (list): Information with order [[name, ID, latitude, longitude]...]
    """

    # Make a request to the web service to get station information
    url = f"https://rse-with-python.arc.ucl.ac.uk/londontube-service/stations/query?id={ids}"
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the CSV response
        csv_data = response.text.strip()
        station_info_matrix = parse_station_data(csv_data)

        return station_info_matrix
    else:
        print(f"Error: Unable to fetch station information for {ids}.")


def query_station_num(station_name):
    """This function takes the name of a station and return its station ID.
    Arg:
        station_name (str): The name of station. eg."Warren street"
    Return:
        station_id (int): The ID of given station.
    """

    # Make a request to the web service to get station information
    url = f"https://rse-with-python.arc.ucl.ac.uk/londontube-service/stations/query?id={station_name}"
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the CSV response
        csv_data = response.text.strip()
        station_info_matrix = parse_station_data(csv_data)
        station_id = station_info_matrix[0][1]

        # return the station id number
        return station_id
    else:
        print(f"Error: Unable to fetch station information for {station_name}.")


def parse_station_data(csv_data):
    """This function converts the csv data of station information to a list.
    Arg:
        csv_data: Station information data obtained from web service.
    Return:
        station_info_matrix (list): Information with order [[name, ID, latitude, longitude]...]
    """

    # Parse the CSV data and return station information as a matrix-like structure
    station_info_matrix = []

    # Use StringIO to convert the CSV data string to a file-like object
    csv_file = StringIO(csv_data)

    # Use the CSV module to read the file-like object
    csv_reader = csv.DictReader(csv_file)

    for row in csv_reader:
        station_info = [
            row["station name"],
            int(row["station index"]),
            float(row["latitude"]),
            float(row["longitude"])
        ]
        station_info_matrix.append(station_info)

    # Sort station information by station index
    station_info_matrix.sort(key=lambda x: x[1])

    return station_info_matrix


def query_disruptions(date_str=None):
    """This function takes a date and query the web service for service disruptions.
    Arg:
        date_str (str): A date in 2023. eg."2023-12-15"
    Return:
        disruptions (list): Disruptions with order [[line, [station1, station2], delay] [None(all the lines), [station], delay]...]
    """
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
        disruptions = parse_disruptions_data(disruptions_data)

        # Print the disruptions matrix
        return disruptions
    else:
        print(f"Error: Unable to fetch disruption information for {date_str}.")


def parse_disruptions_data(disruptions_data):
    """This function converts the service disruptions to a list.
    Arg:
        disruptions_data (dict.): Station information data obtained from web service.
    Return:
        disruptions_ls (list): Disruptions with order [[line, [station1, station2], delay] [None(all the lines), [station], delay]...]
    """
    # Parse the disruption data and return it as a matrix-like structure
    disruptions_ls = []

    for event in disruptions_data:
        disruption = [
            event.get("line"),
            event.get("stations", []),
            event.get("delay", 0)
        ]
        disruptions_ls.append(disruption)

    return disruptions_ls


def real_time_network(date):
    """This function takes a date and return the real-time London tube network on that day.
    Arg:
        date (str): A date in 2023. eg."2023-12-15"
    Return:
        real_time_network (Network): A Network object that represents the London tube network on a particular date.
    """
    disruptions = query_disruptions(date)
    # Init network
    adjacency = np.zeros((296, 296))
    real_time_network = Network(296, adjacency)
    for i in range(12):
        # Network of a particular line
        line_network = query_line_connections(i)
        for j in range(len(disruptions)):
            # For single line
            # Disruption format [[line_idx [station1 station2] delay] x n].
            if disruptions[j][0] == i or disruptions[j][0] is None:
                # Disruption between two stations
                if len(disruptions[j][1]) == 2:
                    station1 = disruptions[j][1][0]
                    station2 = disruptions[j][1][1]
                    delay = disruptions[j][2]
                    # A delay to the direct connection between two stations
                    line_network.adjacency_matrix[station1, station2] *= delay
                # Disruption for 1 station
                else:
                    station = disruptions[j][1]
                    # A delay to all journeys through the station
                    delay = disruptions[j][2]
                    line_network.adjacency_matrix[station, :] *= delay
                    line_network.adjacency_matrix[:, station] *= delay
        # Add real timeline networks together
        real_time_network += line_network

    return real_time_network


"""
 Perform various tasks related to London Tube network analysis and benchmarking.

1. Obtains station connections and creates a weight matrix:
   - `station_list` is populated by querying line connections and extracting station connections.
   - A `weight_matrix` is constructed from the station connections.

2. Benchmarking of network methods:
   - Benchmarking is done for two methods (`Network.distant_neighbours` and a provided method) with varying parameters.
   - Execution times are measured for different 'n' and 'v' values, and average times are calculated.
   - The results are plotted on a log-scale graph.

3. Table output:
   - Tables are generated to display the average execution times for each method based on 'n' and 'v' values.
"""

# Obtain station connections and create a weight matrix
station_list = []
for i in range(12):
    connections_matrix = query_line_connections(i)
    for i in range(connections_matrix.n_nodes):
        for j in range(connections_matrix.n_nodes):
            weight = connections_matrix.adjacency_matrix[i, j]
            if weight > 0:
                station_list.append((i, j, weight))

weight_matrix = np.zeros((296, 296))
for stations in station_list:
    j, i, k = stations
    weight_matrix[i][j] = k
    weight_matrix[j][i] = k

# Benchmarking with varying 'n' and 'v' values
n_values = [1, 2, 3, 4, 5, 7, 8, 10, 12, 14, 17, 20, 25, 29, 35, 42, 51, 61, 73, 87, 104, 125, 149, 179, 214, 256]
v_values = [10, 24, 56, 73, 83, 94, 144, 168, 265]

average_time_network = []
average_time_provided = []

for n_value in n_values:
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

# Table output
table_header = "{:<3} {:<30} {:<30}"
table_separator = "-" * 65
all_tables = []

for v_value_index, v_value in enumerate(v_values):
    current_table = [table_header.format("n", "Network.distant_neighbours (secs)", "Provided method (secs)"),
                     table_separator]

    for n_value_index, n_value in enumerate(n_values):
        times_network = []
        times_provided = []

        for _ in range(3):  # repeating 3 times to get the average data
            start_time_network = time.time()
            Network.distant_neighbours(n_value, v_value, weight_matrix)
            elapsed_time_network = time.time() - start_time_network
            times_network.append(elapsed_time_network)

            start_time_provided = time.time()
            result = distant_neighbours_provided(n_value, v_value, weight_matrix)
            elapsed_time_provided = time.time() - start_time_provided
            times_provided.append(elapsed_time_provided)

        avg_elapsed_time_network = sum(times_network) / len(times_network)
        avg_elapsed_time_provided = sum(times_provided) / len(times_provided)

        current_table.append(f"{n_value:<3} {avg_elapsed_time_network:^30.6f} {avg_elapsed_time_provided:^30.6f}")

    all_tables.append(current_table)

# Output all tables to md file
output_content = ''
for table in all_tables:
    for line in table:
        output_content += str(line) + '\n'

with open('output.md', 'w') as file:
    file.write('# Output 9 tables for Baker Street, Blackfriars, Cockfosters, Earl’s Court, Elephant & Castle, '
               'Finsbury Park, King’s Cross St. Pancras, Morden, Vauxhall respectively\n\n')
    file.write(output_content)
