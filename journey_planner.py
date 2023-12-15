import argparse
import query
from Network import Network
import matplotlib.pyplot as plt
import datetime

def plan_journey(start, dest, date):
    if type(start) == str:
        start_int = query.query_station_num(start)
    else:
        start_int = start
    if type(dest) == str:
        dest_int = query.query_station_num(dest)
    else:
        dest_int = dest
    tube_network = query.real_time_network(date)
    journey, duration = Network.dijkstra(start_int, dest_int, tube_network.adjacency_matrix)
    return journey, duration

def plot_journey(journey, save=False) -> None:
    stations_info = query.query_station_information("all")
    network_lats = []
    network_lons = []
    for i in range(296):
        network_lats.append(stations_info[i][2])
        network_lons.append(stations_info[i][3])

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(network_lons, network_lats, s=1, c="blue", marker="x")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    start_info = query.query_station_information(journey[0])
    dest_info = query.query_station_information(journey[-1])
    start_name = start_info[0][0]
    dest_name = dest_info[0][0]
    plot_title = f"Journey from {start_name} to {dest_name}"
    ax.set_title(f"Journey from {start_name} to {dest_name}")

    # Draw over the network with the journey
    journey_lats = []
    journey_lons = []
    for i in range(len(journey)):
        station_num = journey[i]
        journey_lats.append(stations_info[station_num][2])
        journey_lons.append(stations_info[station_num][3])
    ax.plot(journey_lons, journey_lats, "ro-", markersize=2)
    
    if save:
        plot_filename = f"journey_from_{start_name.replace(' ', '_')}_to_{dest_name.replace(' ', '_')}.png"
        plt.savefig(plot_filename)
        print(f"Plot saved to {plot_filename}")
        plt.show()
    else:
        plt.show()
    return


def journey_planner(args):
    # Need to fill

    print("Start Station:", args.start)
    print("Destination Station:", args.dest)
    print("Setoff Date:", args.setoff_date)
    date = str(args.setoff_date)
    # The journey planner logic
    # When the journey is impossible - given the disruption information.
    # Should return the planned journey, and the time it will take, to the terminal in a human-readable format.
    journey, duration = plan_journey(args.start, args.dest, date)
    print("Journey will take", duration, "minutes.")
    for i in range(len(journey)):
        station_info = query.query_station_information(journey[i])
        if i == 0:
            print("Start:", station_info[0][0])
        elif i == len(journey)-1:
            print("End:", station_info[0][0])
        else:
            print(station_info[0][0])

    # Plot
    plot_journey(journey, args.plot)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Journey Planner Tool")
    parser.add_argument("start", type=str, help="Start station index or name")
    parser.add_argument("dest", type=str, help="Destination station index or name")
    parser.add_argument("--setoff-date", type=str, help="Setoff date in YYYY-MM-DD format (optional)")
    parser.add_argument("--plot", action="store_true", help="Generate and save a plot of the journey")
    
    args = parser.parse_args()
    journey_planner(args)