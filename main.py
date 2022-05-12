#!/usr/bin/env python3

"""Main Bingo module. Which combination of cards has the highest chance to win?"""

from typing import List
from cards import CARDS


def find_permutations(elements: List[int], n: int) -> List[List[int]]:
    """Recursively return all possible permutations (without repetitions) using a set of n integers
    representing arbitrary elements e.g. indices."""

    # Exit condition in case of parameter error
    if n <= 0 or n > len(elements):
        return []

    # Only one level left - return each remaining element as option
    if n == 1:
        return [[x] for x in elements]

    # More iterations necessary - extend result list by each subset
    result: List[List[int]] = []
    for i in range(len(elements)):
        remaining = elements[i + 1:]
        subtree = find_permutations(remaining, n - 1)
        result.extend([[elements[i], *x] for x in subtree])
    return result


def main(num_of_cards: int):
    """Main entry point."""

    # Print card overview
    print("=== Configured Bingo cards ===")
    for i in range(len(CARDS)):
        print("{:>12} {} {}".format(
            CARDS[i].get_name(),
            CARDS[i].draw_terminal_color(),
            " ".join(f"{x:2}" for x in CARDS[i].get_numbers())
        ))
    print()

    # Walk through all permutations
    print(f"=== Finding best combinations for {num_of_cards} card(s). ===")
    combinations: List[List[int]] = find_permutations(range(len(CARDS)), num_of_cards)

    print(f"Total permutations: {len(combinations)}")
    i: int = 0
    for comb in combinations:
        cards = [CARDS[x] for x in comb]
        print(" ".join(f"{x.draw_terminal_color()}" for x in cards))
        i += 1


if __name__ == "__main__":
    num_of_cards: int = 1
    main(num_of_cards)
