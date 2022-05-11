#!/usr/bin/env python3

"""Main Bingo module. Which combination of cards has the highest chance to win?"""

from typing import List
from cards import Card, CARDS


def find_combinations(cards: List[Card], n: int) -> List[List[Card]]:
    """Recursively return all possible permutations using n cards."""

    # Exit condition or parameter error
    if n <= 0 or n > len(cards):
        return []

    # Only one level left - return each remaining card as option
    if n == 1:
        return [[c] for c in cards]

    # More iterations necessary - extend result list by each subset
    result: List[List[Card]] = []
    for i in range(len(cards)):
        remaining = cards[i + 1:]
        subtree = find_combinations(remaining, n - 1)
        result.extend([[cards[i], *sub] for sub in subtree])
    return result


def main():
    """Main entry point."""
    for num in range(1, 6):
        i: int = 0
        print(f"=== Finding best combinations for {num} card(s). ===")
        combinations: List[List[Card]] = find_combinations(CARDS, num)
        for comb in combinations:
            print(i, "+".join(card.get_name() for card in comb))
            i += 1
        print()


if __name__ == "__main__":
    main()
