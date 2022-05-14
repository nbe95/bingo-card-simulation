#!/usr/bin/env python3

"""Bingo simulation module."""

from typing import Any, List, Set, Optional
from random import shuffle
from tqdm import tqdm  # type: ignore
from cards import Card, CARDS


class CardSimu:
    """Wrapper for a card combination and the corresponding simulation score."""

    def __init__(self, combination: Set[int]) -> None:
        self.combination: Set[int] = combination
        self.result: Optional[float] = None

    def set_result(self, score: float) -> None:
        """Set the simulation score for this combination."""
        self.result = score

    def get_result(self) -> float:
        return self.result if self.result else 0

    def get_cards(self) -> Set[Card]:
        """Retreive the global Card objects for this combination."""
        return {CARDS[x] for x in self.combination}


def find_permutations(elements: List[Any], n: int) -> List[Set[Any]]:
    """General function to recursively return all possible permutations
    picking n elements from a given set without repetition."""

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


def print_cards() -> None:
    """Print all available Bingo cards."""

    print("=== Configured Bingo cards ===")
    for card in CARDS:
        print(f"{card.name:>12} {card.draw_terminal_color()} "
              f"{' '.join(f'{x:2}' for x in card.numbers)}")
    print()


def find_combinations(num_of_cards: int) -> List[CardSimu]:
    """Find all possible combinations using n out of all cards."""

    print("=== Finding all combinations ===")
    elements: List[int] = list(range(len(CARDS)))
    combinations: List[CardSimu] = [CardSimu(x) for x in find_permutations(elements, num_of_cards)]
    print(f"Found a total of {len(combinations)} permutations "
          f"taking {num_of_cards} out of {len(CARDS)} cards without repetition.")
    print()
    return combinations


def do_simulation(combinations: List[CardSimu], cycles: int) -> None:
    """Perform simulation for the given combinations."""

    num_of_cards = len(next(iter(combinations[0].get_cards())).numbers)
    print(f"=== Simulating combinations of {num_of_cards} cards ===")

    # Retrieve card deck dynamically from all given cards
    card_deck: List[int] = []
    for card in CARDS:
        card_deck.extend([x for x in card.numbers if x not in card_deck])
    card_deck.sort()

    print(f"Card deck consists of {len(card_deck)} number cards: "
          f"\n  {' '.join(map(str, card_deck))}")
    print(f"Performing {cycles:,} simulation cycles with each permutation.")

    # Test all combinations against thousands of ramdomized card decks...
    iterations: int = len(combinations) * cycles
    with tqdm(total=iterations) as progress:
        for count, perm in enumerate(combinations):
            progress.set_description(f"Permutation {count} of {len(combinations)}")
            perm_total_sum: int = 0
            for _ in range(cycles):
                shuffle(card_deck)
                perm_total_sum += min(x.get_pos_of_last_number(card_deck) for x in perm.get_cards())
                progress.update()
            perm.set_result(perm_total_sum / cycles)
    print()


def print_results(combinations: List[CardSimu], terse: int = 0) -> None:
    """Print pretty statistics and all the other nice stuff we want to see."""

    print("=== Simulation results ===")
    print("Score = Number of card drawings until one of the chosen cards is completed.")
    if terse > 0:
        print(f"Showing only the {terse} best and worst results. "
              f"(Show all with -v flag.)")

    combinations.sort(key=lambda x: x.get_result(), reverse=False)
    for i, comb in enumerate(combinations):
        if terse == 0 or i < terse or i >= len(combinations) - terse:
            print(f"{i+1:11}: {' '.join(f'{x.draw_terminal_color()}' for x in comb.get_cards())} "
                  f"Score = {comb.result:.3f}"
                  f"{' (best)' if i == 0 else ''}"
                  f"{' (worst)' if i == len(combinations) - 1 else ''}")

        elif terse > 0 and i == terse:
            print()
