#!/usr/bin/env python3

"""Main Bingo module. Which combination of cards has the highest chance to win?"""

from typing import Any, List, Set
from cards import Card, CARDS


def find_permutations(elements: List[Any], n: int) -> List[List[Any]]:
    """Recursively return all possible permutations picking n elements from a given
    set without repetition."""

    # Exit condition in case of parameter error
    if n <= 0 or n > len(elements):
        return []

    # Only one level left - return each remaining element as option
    if n == 1:
        return [[x] for x in elements]

    # More iterations necessary - extend result list by each subset
    result: List[List[Any]] = []
    for i, element in enumerate(elements):
        remaining: List[Any] = elements[i + 1:]
        subtree: List[List[Any]] = find_permutations(remaining, n - 1)
        result.extend([[element, *x] for x in subtree])
    return result


def main(num_of_cards: int = 1, simu_cycles: int = 10000):
    """Main entry point."""

    # Print card overview
    print("=== Configured Bingo cards ===")
    for card in CARDS:
        print(f"{card.get_name():>12} {card.draw_terminal_color()} "
              f"{' '.join(f'{x:2}' for x in card.get_numbers())}")
    print()

    # Walk through all permutations
    print(f"=== Finding best combinations for {num_of_cards} card(s). ===")
    elements: Set[int] = set(range(len(CARDS)))
    combinations: List[Set[int]] = [set(x) for x in find_permutations(list(elements), num_of_cards)]

    print(f"Total permutations: {len(combinations)}")
    for count, perm in enumerate(combinations):
        cards: List[Card] = [CARDS[x] for x in perm]
        print(f"{count+1:5}: {'+'.join(f'{x.draw_terminal_color()}' for x in cards)}")


if __name__ == "__main__":
    main()
