"""Parity check for 8-Puzzle states (Aufgabe 1).

An 8-Puzzle configuration is solvable if and only if the number of inversions
in the tile sequence (ignoring the blank) is even.
"""

from __future__ import annotations

from puzzle8.puzzle import Board


def count_inversions(board: Board) -> int:
    """Count the number of inversions in *board* (blank tile excluded).

    An inversion is a pair (i, j) where i < j but board[i] > board[j],
    considering only non-zero tiles.

    Examples:
        >>> count_inversions((1, 2, 4, 3, 5, 6, 7, 8, 0))
        1
        >>> count_inversions((7, 2, 4, 5, 0, 6, 8, 3, 1))
        16
    """
    tiles = [t for t in board if t != 0]
    return sum(
        1
        for i in range(len(tiles))
        for j in range(i + 1, len(tiles))
        if tiles[i] > tiles[j]
    )


def is_solvable(board: Board) -> bool:
    """Return True if *board* is reachable from the goal state.

    Uses parity: a configuration is solvable iff its inversion count is even.

    Examples:
        >>> from puzzle8.puzzle import GOAL_STATE
        >>> is_solvable(GOAL_STATE)
        True
        >>> is_solvable((7, 2, 4, 5, 0, 6, 8, 3, 1))
        True
        >>> is_solvable((1, 2, 4, 3, 5, 6, 7, 8, 0))
        False
    """
    return count_inversions(board) % 2 == 0
