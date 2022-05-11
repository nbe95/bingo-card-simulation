#!/usr/bin/env python3

"""Bingo Card module."""

from typing import List
from colour import Color  # type: ignore


class Card:
    """Class for each Bingo card."""
    def __init__(self, name: str, color: Color, fields: List[int]) -> None:
        self.name: str = name
        self.color: Color = color
        self.fields: List[int] = fields

    def get_name(self) -> str:
        """Return the card's name."""
        return self.name

    def get_color(self) -> Color:
        """Return the card's color."""
        return self.color

    def get_fields(self) -> List[int]:
        """Return the card's fields."""
        return self.fields

    def draw_terminal_color(self) -> str:
        """Return a color representing field of spaces for ANSI terminals."""
        rgb: List[int] = [int(c * 255) for c in self.color.rgb]
        return f"\x1b[48;2;{';'.join(map(str, rgb))}m  \x1b[0m"


CARDS: List[Card] = [
    Card("Rot", Color("#cc0044"), [11, 27, 1, 24, 14, 18, 21, 4, 9]),
    Card("Rosa", Color("#ff88cc"), [29, 19, 13, 6, 10, 22, 3, 15, 28]),
    Card("Hellblau", Color("#0088ff"), [17, 30, 20, 7, 1, 12, 25, 8, 29]),
    Card("Hellgelb", Color("#ffff80"), [14, 8, 2, 23, 11, 25, 4, 29, 17]),
    Card("Grün", Color("#008800"), [16, 2, 19, 28, 9, 23, 12, 7, 30]),
    Card("Violett", Color("#880088"), [12, 24, 3, 5, 16, 21, 20, 27, 8]),
    Card("Gelb", Color("#cccc00"), [26, 22, 7, 1, 17, 27, 13, 20, 10]),
    Card("Grau", Color("#888888"), [9, 14, 6, 22, 4, 15, 30, 18, 26]),
    Card("Blau", Color("#00ffff"), [15, 3, 23, 25, 6, 11, 18, 28, 5]),
    Card("Orange", Color("#ffaa00"), [5, 16, 19, 21, 2, 13, 26, 10, 24])
]
