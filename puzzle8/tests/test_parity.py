"""Tests for parity.py — inversion counting and solvability."""

import pytest
from puzzle8.parity import count_inversions, is_solvable


def test_goal_state_zero_inversions() -> None:
    """Goal state has 0 inversions and is solvable."""
    from puzzle8.puzzle import GOAL_STATE
    assert count_inversions(GOAL_STATE) == 0
    assert is_solvable(GOAL_STATE)


def test_single_swap_unsolvable() -> None:
    """Swapping two adjacent tiles produces an unsolvable state."""
    # Swap tiles 1 and 2 in the goal state → 1 inversion → unsolvable
    unsolvable: tuple[int, ...] = (2, 1, 3, 4, 5, 6, 7, 8, 0)
    assert not is_solvable(unsolvable)
