import argparse

from queens_solver import solve_queens
from tango_solver import solve_tango

def initialize_parser():
    parser = argparse.ArgumentParser(description="Solve LinkedIn Game")
    parser.add_argument(
        "--game",
        type=str,
        help="The game to solve. Options: 'zip', 'queens', 'tango', 'pinpoint', or 'crossclimb'.",
        choices=["zip", "queens", "tango", "pinpoint", "crossclimb"],
        required=True,
    )
    return parser

def main():
    parser = initialize_parser()
    args = parser.parse_args()

    if args.game == "zip":
        print("Game 'zip' is not implemented yet.")
    elif args.game == "queens":
        solve_queens()
    elif args.game == "tango":
        solve_tango()
    elif args.game == "pinpoint":
        print("Game 'pinpoint' is not implemented yet.")
    elif args.game == "crossclimb":
        print("Game 'crossclimb' is not implemented yet.")
    else:
        print("Invalid game option. Please choose from 'zip', 'queens', 'tango', 'pinpoint', or 'crossclimb'.")
        return 

if __name__ == "__main__":
    main()
