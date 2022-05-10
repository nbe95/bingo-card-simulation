"""Bingo Card module."""

from typing import List


class Card:
    """Class for each Bingo card."""
    def __init__(self, name: str, color: str, fields: List[int]) -> None:
        self.name: str = name
        self.color: str = color
        self.fields: List[int] = fields
