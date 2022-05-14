#!/usr/bin/env python3

"""Main Bingo module. Which combination of cards has the highest chance to win?"""

import argparse
from typing import Any, List, Set, Tuple
from random import shuffle
import sys
from tqdm import tqdm  # type: ignore
from cards import Card, CARDS


def options() -> argparse.Namespace:
    """Wrapper for CLI argument parsing."""

    parser = argparse.ArgumentParser(
        description="Bingo card combination simulator. "
                    "Which combination of cards has the highest chance to win?")

    parser.add_argument("num_of_cards", type=int,
                        help="number of cards in each set to be analyzed")
    parser.add_argument("-c", "--simu_cycles", type=int, default=100000,
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


def print_cards(cards: List[Card]) -> None:
    """Print all available Bingo cards."""

    print("=== Configured Bingo cards ===")
    for card in cards:
        print(f"{card.name:>12} {card.draw_terminal_color()} "
              f"{' '.join(f'{x:2}' for x in card.numbers)}")
    print()


def find_combinations(cards: List[Card], num_of_cards: int) -> List[Set[int]]:
    """Find all possible combinations using n out of all cards."""

    print("=== Finding all combinations ===")
    elements: Set[int] = set(range(len(cards)))
    combinations: List[Set[int]] = find_permutations(list(elements), num_of_cards)
    print(f"Found a total of {len(combinations)} permutations "
          f"taking {num_of_cards} out of {len(cards)} cards without repetition.")
    print()
    return combinations


def do_simulation(cards: List[Card], combinations: List[Set[int]],
                  cycles: int) -> List[Tuple[Set[int], float]]:
    """Perform simulation for the given combinations."""

    print(f"=== Simulating combinations of {len(combinations[0])} cards ===")

    # Retrieve card deck dynamically from all given cards
    card_deck: List[int] = []
    for card in cards:
        card_deck.extend([x for x in card.numbers if x not in card_deck])
    card_deck.sort()

    print(f"Card deck consists of {len(card_deck)} number cards: "
          f"\n  {' '.join(map(str, card_deck))}")
    print(f"Performing {cycles:,} simulation cycles with each permutation.")

    # Test all combinations against thousands of ramdomized card decks...
    results: List[Tuple[Set[int], float]] = []
    iterations: int = len(combinations) * cycles
    with tqdm(total=iterations) as progress:
        for count, perm in enumerate(combinations):
            progress.set_description(f"Permutation {count} of {len(combinations)}")
            perm_total_sum: int = 0
            for _ in range(cycles):
                shuffle(card_deck)
                perm_total_sum += max(CARDS[x].get_pos_of_last_number(card_deck) for x in perm)
                progress.update()
            results.append((perm, perm_total_sum / cycles))
    print()
    return results


def print_results(results: List[Tuple[Set[int], float]], terse: int = 0) -> None:
    """Print pretty statistics and all the other stuff we wanted to see."""

    print("=== Simulation results ===")
    print("Score = Number of card drawings until one of the chosen cards is completed.")
    if terse > 0:
        print(f"Showing only the {terse} best and worst results. "
              f"(Show all with -v flag.)")

    results.sort(key=lambda x: x[1], reverse=False)
    for i, result in enumerate(results):
        if terse == 0 or i < terse or i >= len(results) - terse:
            cards: List[Card] = [CARDS[x] for x in result[0]]
            score: float = result[1]
            print(f"{i+1:10}: {' '.join(f'{x.draw_terminal_color()}' for x in cards)} "
                  f"Score = {score:.3f}")

        elif terse > 0 and i == terse:
            print()


def main(args: argparse.Namespace) -> None:
    """Main entry point."""

    # Catch Ctrl+C as exit condition
    try:
        print_cards(CARDS)
        combinations = find_combinations(CARDS, args.num_of_cards)
        results = do_simulation(CARDS, combinations, args.simu_cycles)
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
