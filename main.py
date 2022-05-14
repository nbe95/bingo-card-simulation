#!/usr/bin/env python3

"""Main Bingo module. Which combination of cards has the highest chance to win?"""

import argparse
from typing import Any, List, Set, Tuple
import sys
from cards import CARDS
from simulation import print_cards, find_combinations, do_simulation, print_results


def options() -> argparse.Namespace:
    """Wrapper for CLI argument parsing."""

    parser = argparse.ArgumentParser(
        description="An awesome Bingo card combination simulator! "
                    "Which combination of cards has the highest chance to win?")

    parser.add_argument("num_of_cards", type=int,
                        help="number of cards in each set to be analyzed")
    parser.add_argument("-c", "--simu_cycles", type=int, default=100000,
                        help="number of simulation cycles for each combination")
    parser.add_argument("-v", "--verbose-results", action='store_true',
                        help="show all results instead of summary list")

    return parser.parse_args()


def main(args: argparse.Namespace) -> None:
    """Main entry point."""

    # Catch Ctrl+C as exit condition
    try:
        print_cards()
        combinations = find_combinations(args.num_of_cards)
        results = do_simulation(combinations, args.simu_cycles)
        print_results(results, 0 if args.verbose_results else 10)

    except KeyboardInterrupt:
        print("Simulation aborted.")
        sys.exit(1)


if __name__ == "__main__":
    opt: argparse.Namespace = options()
    if opt.num_of_cards not in range(1, len(CARDS) + 1):
        raise argparse.ArgumentTypeError(
            f"Invalid number of cards supplied. (Valid: 1..{len(CARDS)})")

    main(opt)
