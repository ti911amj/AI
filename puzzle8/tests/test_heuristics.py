"""Tests for heuristics.py — h1 (misplaced tiles) and h2 (Manhattan)."""

import pytest
from puzzle8.puzzle import GOAL_STATE
from puzzle8.heuristics import h1, h2


def test_h1_goal_is_zero() -> None:
    assert h1(GOAL_STATE) == 0


def test_h2_goal_is_zero() -> None:
    assert h2(GOAL_STATE) == 0


def test_h1_counts_misplaced() -> None:
    # Move blank left: (1,2,3,4,5,6,7,0,8) — tile 8 is misplaced
    board = (1, 2, 3, 4, 5, 6, 7, 0, 8)
    assert h1(board) == 1


def test_h2_manhattan_one_move() -> None:
    # Same board as above — tile 8 is one step away from goal
    board = (1, 2, 3, 4, 5, 6, 7, 0, 8)
    assert h2(board) == 1


def test_h2_geq_h1() -> None:
    """h2 dominates h1 — Manhattan is always >= misplaced tiles."""
    board = (8, 7, 6, 5, 4, 3, 2, 1, 0)
    assert h2(board) >= h1(board)
