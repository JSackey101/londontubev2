import requests
from datetime import date
import csv
from io import StringIO
import numpy as np
from .Network import Network




def query_line_connections(line_identifier):
    """This function takes the line identifier, quering the web service for information 
    about the connectivity of a particular line, and returns a Network object 
    that represents that line.

    Parameters
    ----------
    line_identifier: int
        The ID for a particular line in London tube network
    
    Returns
    -------
    line_network
        A network object of the line, i.e. a sub-network of London tube
    
    Examples
    --------
    >>> from query import query_line_connections
    >>> Bakerloo = query_line_connections(0)
    """
    # Check input type
    if not isinstance(line_identifier, int):
        raise TypeError("The line identifier must be an integer.")
    if not 0 <= line_identifier <= 11:
        raise ValueError("Line ID must be in the range 0 to 11")
    
    # Check internet connection
    try:
        requests.get("https://www.google.com", timeout=5)
    except requests.ConnectionError:
        raise ConnectionError("No internet connection. Please check your network.")

    # Make a request to the web service to get line connections
    url = f"https://rse-with-python.arc.ucl.ac.uk/londontube-service/line/query?line_identifier={line_identifier}"
    response = requests.get(url)

    # Init a adjacency matrix with 296x296 (296 stations in London tube network)
    adjacency = np.zeros((296,296))

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
        # No informaiton for given line 
        raise ValueError(f"Error: Unable to fetch line connections for {line_identifier}.")


def query_station_information(ids):
    """
    This function takes the station ID and queries the web service for station information.

    Parameters
    ----------
    ids : int, np.int32, str
        The ID for station/stations in London tube network. For example, 1 (int), "all" (str), "1, 3, 7" (str).
    
    Returns
    -------
    station_info_matrix : list
        Information with order [[name, ID, latitude, longitude]...].
    """
    # Check input type
    if not isinstance(ids, (np.int32, int, str)):
        raise TypeError("The station must be an integer or string.")
    
    # Check input value
    if isinstance(ids, (int, np.int32)):
        # 296 stations in total. Index from 0 to 195
        if not 0 <= ids <= 295:
            raise ValueError("Line ID must be in the range 0 to 295")
    
    # Check internet connction
    try:
        requests.get("https://www.google.com", timeout=5)
    except requests.ConnectionError:
        raise ConnectionError("No internet connection. Please check your network.")
    
    # Make a request to the web service to get station information
    url = f"https://rse-with-python.arc.ucl.ac.uk/londontube-service/stations/query?id={ids}"
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the CSV response
        csv_data = response.text.strip()
        station_info_matrix = parse_station_data(csv_data)

        return station_info_matrix
    else:
        # No informaiton for given station
        raise ValueError(f"Error: Unable to fetch station information for {ids}.")

def query_station_num(station_name):
    """
    This function takes the name of a station and returns its station ID.

    Parameters
    ----------
    station_name : str
        The name of the station. For example, "Warren Street".

    Returns
    -------
    station_id : int
        The ID of the given station.
    """
    # Check input type
    if not isinstance(station_name, str):
        raise TypeError("The station name must be an string.")
    
    # Check internet connection
    try:
        requests.get("https://www.google.com", timeout=5)
    except requests.ConnectionError:
        raise ConnectionError("No internet connection. Please check your network.")
    
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
        # No informaiton for given station name
        raise ValueError(f"Error: Unable to fetch station information for {station_name}.")

def parse_station_data(csv_data):
    """
    This function converts the csv data of station information into a list.

    Parameters
    ----------
    csv_data : str
        Station information data obtained from the web service in CSV format.

    Returns
    -------
    list
        A list of station information, formatted as [[name, ID, latitude, longitude]...].
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
    """
    This function takes a date and queries the web service for service disruptions.

    Parameters
    ----------
    date_str : str, optional
        A date in the format 'YYYY-MM-DD' (default is None). For example, "2023-12-15".

    Returns
    -------
    list
        A list of service disruptions. Each disruption is represented as 
        [line, [station1, station2], delay] or [None (indicating all lines), [station], delay].
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
                raise ValueError("Provided date outside the valid range. Valid range is from 2023-1-1 to 2023-12-31")
        except ValueError:
            raise ValueError("Date provided is in the wrong format. Correct format would be 'YYYY-MM-DD' ")

    # Check internet connection
    try:
        requests.get("https://www.google.com", timeout=5)
    except requests.ConnectionError:
        raise ConnectionError("No internet connection. Please check your network.")

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
    """
    This function converts the service disruptions data into a list.

    Parameters
    ----------
    disruptions_data : dict
        Service disruptions information obtained from the web service.

    Returns
    -------
    list
        A list of service disruptions. Each disruption is represented as 
        [line, [station1, station2], delay] or [None (indicating all lines), [station], delay].
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
    """
    This function takes a date and returns the real-time London tube network on that day.

    Parameters
    ----------
    date : str
        A date in the format 'YYYY-MM-DD'. For example, "2023-12-15".

    Returns
    -------
    Network
        A Network object representing the London tube network on the specified date.
    """
    disruptions = query_disruptions(date)
    # Init network
    adjacency = np.zeros((296,296))
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
                    line_network.adjacency_matrix[station1,station2] *= delay
                # Disruption for 1 station
                else:
                    station = disruptions[j][1]
                    # A delay to all journeys through the station
                    delay = disruptions[j][2]
                    line_network.adjacency_matrix[station, :] *= delay
                    line_network.adjacency_matrix[:, station] *= delay
        # Add real time line networks together
        real_time_network += line_network        
    return real_time_network


