#!/usr/bin/env python3

"""Main Bingo module. Which combination of cards has the highest chance to win?"""

import argparse
from time import sleep
from typing import Any, List, Set
from tqdm import tqdm  # type: ignore
from cards import Card, CARDS


def options() -> argparse.Namespace:
    """Wrapper for CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description="Bingo card combination simulator. "
                    "Which combination of cards has the highest chance to win?")

    parser.add_argument("--num_of_cards", "-n", type=int, default=2,
                        help="number of cards in each set to be analyzed")
    parser.add_argument("--simu_cycles", "-c", type=int, default=100000,
                        help="number of simulation cycles for each combination")

    return parser.parse_args()


def find_permutations(elements: List[Any], n: int) -> List[Set[Any]]:
    """Recursively return all possible permutations picking n elements from a given
    set without repetition."""

    # Exit condition in case of parameter error
    if n <= 0 or n > len(elements):
        return []

    # Only one level left - return each remaining element as option
    if n == 1:
        return [{x} for x in elements]

    # More iterations necessary - extend result list by each subset
    result: List[Set[Any]] = []
    for i, element in enumerate(elements):
        remaining: List[Any] = elements[i + 1:]
        subtree: List[Set[Any]] = find_permutations(remaining, n - 1)
        result.extend([{element, *x} for x in subtree])
    return result


def main(args: argparse.Namespace) -> None:
    """Main entry point."""

    # Print card overview
    print("=== Configured Bingo cards ===")
    for card in CARDS:
        print(f"{card.get_name():>12} {card.draw_terminal_color()} "
              f"{' '.join(f'{x:2}' for x in card.get_numbers())}")
    print()

    # Find all possible combinations/permutations
    print(f"=== Simulating combinations of {args.num_of_cards} cards ===")
    elements: Set[int] = set(range(len(CARDS)))
    combinations: List[Set[int]] = find_permutations(list(elements), args.num_of_cards)
    print(f"Found a total of {len(combinations)} permutations.")

    # Do something with the permutations...
    print(f"Performing {args.simu_cycles:,} simulation cycles with each permutation.")
    with tqdm(total=len(combinations)) as progress:
        for _ in combinations:
            sleep(0.1)
            progress.update()
    print()

    # Print results
    print("=== Simulation results ===")
    for count, perm in enumerate(combinations):
        cards: List[Card] = [CARDS[x] for x in perm]
        print(f"{count+1:5}: {'+'.join(f'{x.draw_terminal_color()}' for x in cards)}")


if __name__ == "__main__":
    main(options())
