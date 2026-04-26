"""Tests for puzzle.py — board representation and neighbor generation."""

import pytest
from puzzle8.puzzle import Board, GOAL_STATE, blank_index, neighbors, random_state


def test_blank_index_goal() -> None:
    """Blank tile is at index 8 in the goal state."""
    assert blank_index(GOAL_STATE) == 8


def test_neighbors_goal_state() -> None:
    """Goal state has exactly 2 neighbors (corner position)."""
    result = list(neighbors(GOAL_STATE))
    assert len(result) == 2


def test_random_state_is_solvable() -> None:
    """random_state() should always return a solvable board."""
    from puzzle8.parity import is_solvable
    for seed in range(20):
        assert is_solvable(random_state(seed=seed))
