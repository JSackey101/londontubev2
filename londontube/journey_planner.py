import argparse
from . import query
from .Network import Network
import matplotlib.pyplot as plt
from datetime import date

def plan_journey(start, dest, date):
    """
    Calculate the path and duration of a journey given the start point, destination, and date.

    Parameters
    ----------
    start : int or str
        The ID or name of the start station.
    dest : int or str
        The ID or name of the destination station.
    date : str
        The date of the journey in 'YYYY-MM-DD' format.

    Returns
    -------
    tuple of (list of int, float)
        A tuple where the first element is a list that includes the IDs of passing stations in order,
        and the second element is the duration of the journey in minutes.
    """
    # If start or dest is a str, then convert it to station ID
    if type(start) == str:
        start_int = query.query_station_num(start)
    else:
        start_int = start
    if type(dest) == str:
        dest_int = query.query_station_num(dest)
    else:
        dest_int = dest
    # The london tube network of given date
    tube_network = query.real_time_network(date)
    # Apply dij to obtain the path and time
    journey, duration = Network.dijkstra(start_int, dest_int, tube_network.adjacency_matrix)
    return journey, duration

def plot_journey(journey, save=False) -> None:
    """
    Plot a figure to visualize the journey path.

    Parameters
    ----------
    journey : list of int/np.int32
        IDs of passing stations in the journey.
    save : bool, optional
        If True, the figure will be saved. Default is False.
    """
    # Obtain all stations' information.
    stations_info = query.query_station_information("all")

    # Lists for lats and lons of the stations in London tube network
    network_lats = []
    network_lons = []
    for i in range(296):
        network_lats.append(stations_info[i][2])
        network_lons.append(stations_info[i][3])
    
    # Plot all the stations 
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(network_lons, network_lats, s=1, c="blue", marker="x")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    
    # Title of the plot
    start_info = query.query_station_information(journey[0])
    dest_info = query.query_station_information(journey[-1])
    start_name = start_info[0][0]
    dest_name = dest_info[0][0]
    ax.set_title(f"Journey from {start_name} to {dest_name}")

    # Draw over the network with the journey
    journey_lats = []
    journey_lons = []
    for i in range(len(journey)):
        station_num = journey[i]
        journey_lats.append(stations_info[station_num][2])
        journey_lons.append(stations_info[station_num][3])
    ax.plot(journey_lons, journey_lats, "ro-", markersize=2)
    
    # Save the figure if necessary
    if save:
        plot_filename = f"journey_from_{start_name.replace(' ', '_')}_to_{dest_name.replace(' ', '_')}.png"
        plt.savefig(plot_filename)
        print(f"Plot saved to {plot_filename}")
        plt.show()
    else:
        plt.show()
    return


def journey_planner(plot, start, dest, setoff_date):
    """
    This function takes arguments from parser(--plot(optional) start dest setoff_date(optional, defalt is today)), 
    and visulize the journey information.

    Parameters
    ----------
    plot : bool
        If it is true then plot the figure for the journey and save as png file.
    start : int or str
        The ID or name of the start station.
    dest : int or str
        The ID or name of the destination station.
    setoff_date : str
        The date of the journey in 'YYYY-MM-DD' format.
    """

    print("Date:", setoff_date)
    journey, duration = plan_journey(start, dest, setoff_date)
    if journey == None:
        print("This journey is impossible due to disruptions on the given date")
        exit()  
    print(f"Journey will take {duration:.0f} minutes.")
    for i in range(len(journey)):
        station_info = query.query_station_information(journey[i])
        if i == 0:
            print("Start:", station_info[0][0])
        elif i == len(journey)-1:
            print("End:", station_info[0][0])
        else:
            print(station_info[0][0])

    # Plot
    if plot:
        plot_journey(journey, plot)

def process():
    parser = argparse.ArgumentParser(description="Journey Planner Tool")
    parser.add_argument("--plot", action="store_true", help="Generate and save a plot of the journey")
    parser.add_argument("start", type=str, help="Start station index or name")
    parser.add_argument("dest", type=str, help="Destination station index or name")
    parser.add_argument("setoff_date", nargs='?', default=str(date.today()), type=str, help="Setoff date in YYYY-MM-DD format (optional)")
    args = parser.parse_args()
    journey_planner(args.plot, args.start, args.dest, args.setoff_date)

if __name__ == "__main__":
    process()