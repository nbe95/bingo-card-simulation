#!/usr/bin/env python3

"""Main Bingo module. Which combination of cards has the highest chance to win?"""

from typing import List
from cards import Card

CARDS: List[Card] = [
    Card("rot", "#d90655", [11, 27, 1, 24, 14, 18, 21, 4, 9]),
    Card("rosa", "#9f9699", [29, 19, 13, 6, 10, 22, 3, 15, 28]),
    Card("hellblau", "#7291ae", [17, 30, 20, 7, 1, 12, 25, 8, 29]),
    Card("hellgelb", "#aeab82", [14, 8, 2, 23, 11, 25, 4, 29, 17]),
    Card("grün", "#054f10", [16, 2, 19, 28, 9, 23, 12, 7, 30]),
    Card("violett", "#c72393", [12, 24, 3, 5, 16, 21, 20, 27, 8]),
    Card("gelb", "#bea600", [26, 22, 7, 1, 17, 27, 13, 20, 10]),
    Card("grau", "#9ea4a3", [9, 14, 6, 22, 4, 15, 30, 18, 26]),
    Card("blau", "#0077bb", [15, 3, 23, 25, 6, 11, 18, 28, 5]),
    Card("orange", "#c18000", [5, 16, 19, 21, 2, 13, 26, 10, 24])
]


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
            print(i, "+".join(card.name for card in comb))
            i += 1
        print()


if __name__ == "__main__":
    main()
