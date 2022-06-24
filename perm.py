#!/usr/bin/env python3

"""General helper script to handle finding of permutations."""


from typing import List, Sequence, Any


def find_permutations(
    elements: Sequence[Any], n: int, repetition: bool = True
) -> List[Sequence[Any]]:
    """
    General function to find all possible permutations of a generic set recursively.

    A specific number of elements will be picked from the given sequence with or
    without repetition, as configured.
    """
    # Exit condition or parameter error
    if n <= 0 or len(elements) == 0:
        return []

    # Only one level left - return each remaining element as option
    if n == 1:
        return [[x] for x in elements]

    # More iterations necessary - extend result list by each available subset
    result: List[Sequence[Any]] = []
    for i, element in enumerate(elements):
        subtree: List[Sequence[Any]] = find_permutations(
            elements if repetition else elements[i + 1:], n - 1, repetition
        )
        result.extend([[element, *x] for x in subtree])
    return result
