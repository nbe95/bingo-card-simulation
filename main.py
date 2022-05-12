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


def main():
    """Main entry point."""
    for num in range(1, 6):
        i: int = 0
        print(f"=== Finding best combinations for {num} card(s). ===")
        combinations: List[List[int]] = find_permutations(range(len(CARDS)), num)
        for comb in combinations:
            cards = [CARDS[x] for x in comb]
            print(i, " ".join(f"{x.draw_terminal_color()}{x.get_name():8}" for x in cards))
            i += 1
        print()


if __name__ == "__main__":
    main()
