import requests
from datetime import date
import csv
from io import StringIO




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
            # Print information about the resulting connections
        if connections:
            print(f"Connections for the {line_identifier} line:")
            for connection in connections:
                print(connection)
            print()
        else:
            print(f"No connections found for the {line_identifier} line.")
    else:
        print(f"Error: Unable to fetch line connections for {line_identifier}.")
        return None


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
        print_matrix(station_info_matrix)
    else:
        print(f"Error: Unable to fetch station information for {ids}.")

def parse_station_data(csv_data):
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

