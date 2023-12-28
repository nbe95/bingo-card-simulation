#!/usr/bin/env python3

"""Bingo Card module."""

from typing import List, Tuple

from colour import Color

BingoNumbers = Tuple[int, int, int, int, int, int, int, int, int]


class Card:
    """Class for a Bingo card."""

    def __init__(self, name: str, color: Color, numbers: BingoNumbers) -> None:
        """Construct a Bingo card."""
        self.name: str = name
        self.color: Color = color
        self.numbers: BingoNumbers = numbers

    def get_pos_of_last_number(self, card_deck: List[int]) -> int:
        """Indicate a card's level of strength.

        This function gets the position of this card's last drawn number in a
        given card set.
        This is the total number of iterations this card needs to be completely
        solved.
        """
        # Iterate over the card deck and abort if there's a matching number on
        # this card. Note: It makes no difference whether we check for the
        # first or last occurrence of this number.
        for index, number in enumerate(card_deck):
            if number in self.numbers:
                # Increase performance by iterating from the front,
                # but pretend to do so in backward order (hence subtract).
                return len(card_deck) - index
        return 0

    def draw_terminal_color(self) -> str:
        """Return a color representing field of spaces for ANSI terminals."""
        rgb: List[int] = [int(c * 255) for c in self.color.rgb]
        return f"\x1b[48;2;{';'.join(map(str, rgb))}m  \x1b[0m"


# Global card list
CARDS: List[Card] = [
    Card("Red", Color("#cc0044"), (11, 27, 1, 24, 14, 18, 21, 4, 9)),  # noqa
    Card("Pink", Color("#ff88cc"), (29, 19, 13, 6, 10, 22, 3, 15, 28)),  # noqa
    Card(
        "Light blue", Color("#00ffff"), (17, 30, 20, 7, 1, 12, 25, 8, 29)
    ),  # noqa
    Card(
        "Light yellow", Color("#ffff88"), (14, 8, 2, 23, 11, 25, 4, 29, 17)
    ),  # noqa
    Card("Green", Color("#008800"), (16, 2, 19, 28, 9, 23, 12, 7, 30)),  # noqa
    Card(
        "Purple", Color("#880088"), (12, 24, 3, 5, 16, 21, 20, 27, 8)
    ),  # noqa
    Card(
        "Yellow", Color("#cccc00"), (26, 22, 7, 1, 17, 27, 13, 20, 10)
    ),  # noqa
    Card("Gray", Color("#888888"), (9, 14, 6, 22, 4, 15, 30, 18, 26)),  # noqa
    Card("Blue", Color("#0088ff"), (15, 3, 23, 25, 6, 11, 18, 28, 5)),  # noqa
    Card(
        "Orange", Color("#ffaa00"), (5, 16, 19, 21, 2, 13, 26, 10, 24)
    ),  # noqa
]
