import argparse

def journey_planner(args):
    # Need to fill

    print("Start Station:", args.start)
    print("Destination Station:", args.destination)
    print("Setoff Date:", args.setoff_date)

    # The journey planner logic
    # When the journey is impossible - given the disruption information.
    # Should return the planned journey, and the time it will take, to the terminal in a human-readable format.
    
    # Plot
    if args.plot:
        plot_filename = f"journey_from_{args.start.replace(' ', '_')}_to_{args.destination.replace(' ', '_')}.png"
        plt.savefig(plot_filename)
        print(f"Plot saved to {plot_filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Journey Planner Tool")
    parser.add_argument("start", type=str, help="Start station index or name")
    parser.add_argument("destination", type=str, help="Destination station index or name")
    parser.add_argument("--setoff-date", type=str, default=datetime.now().strftime("%Y-%m-%d"), help="Setoff date in YYYY-MM-DD format (optional)")
    parser.add_argument("--plot", action="store_true", help="Generate and save a plot of the journey")
    
    args = parser.parse_args()
    journey_planner(args)

