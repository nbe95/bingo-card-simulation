#!/usr/bin/env python3

"""Main Bingo module. Which combination of cards has the highest chance to win?"""

import argparse
from time import sleep
from typing import Any, List, Set, Tuple
from tqdm import tqdm  # type: ignore
from cards import Card, CARDS
from random import shuffle


def options() -> argparse.Namespace:
    """Wrapper for CLI argument parsing."""
    parser = argparse.ArgumentParser(
        description="Bingo card combination simulator. "
                    "Which combination of cards has the highest chance to win?")

    parser.add_argument("num_of_cards", type=int,
                        help="number of cards in each set to be analyzed")
    parser.add_argument("-c", "--simu_cycles", type=int, default=10000,
                        help="number of simulation cycles for each combination")
    parser.add_argument("-v", "--verbose-results", action='store_true',
                        help="show all results instead of summary list")

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
        print(f"{card.name:>12} {card.draw_terminal_color()} "
              f"{' '.join(f'{x:2}' for x in card.numbers)}")
    print()

    # Find all possible combinations/permutations
    print(f"=== Simulating combinations of {args.num_of_cards} cards ===")
    elements: Set[int] = set(range(len(CARDS)))
    combinations: List[Set[int]] = find_permutations(list(elements), args.num_of_cards)
    print(f"Performing {args.simu_cycles:,} simulation cycles "
          f"with a total set of {len(combinations)} permutations.")

    # Retrieve card deck dynamically from all given cards
    card_deck: List[int] = []
    for card in CARDS:
        card_deck.extend([x for x in card.numbers if x not in card_deck])
    card_deck.sort()

    # Test all combinations against thousands of ramdomized card decks...
    total_results: List[Tuple[Set[int], float]] = []
    iterations: int = len(combinations) * args.simu_cycles
    with tqdm(total=iterations) as progress:
        for perm in combinations:
            perm_results: List[int] = []
            for _ in range(args.simu_cycles):
                shuffle(card_deck)
                card_results: Tuple[int, ...] = (CARDS[x].get_pos_of_last_number(card_deck)
                                                for x in perm)
                perm_results.append(max(card_results))
                progress.update()
            total_results.append((perm, sum(perm_results) / len(perm_results)))
    print()

    # Print results
    print("=== Simulation results ===")
    total_results.sort(key=lambda x: x[1], reverse=False)
    for i, result in enumerate(total_results):
        cards: List[Card] = [CARDS[x] for x in result[0]]
        score: float = result[1]
        print(f"{i+1:10}: {' '.join(f'{x.draw_terminal_color()}' for x in cards)} - "
              f"score = {score:.3f}")


if __name__ == "__main__":
    opt: argparse.Namespace = options()
    if opt.num_of_cards not in range(1, len(CARDS) + 1):
        raise argparse.ArgumentTypeError(
            f"Invalid number of cards supplied. (Valid: 1..{len(CARDS)})")

    main(opt)
