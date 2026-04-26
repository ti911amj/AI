"""Tests for ids.py — Iterative Deepening Search."""

import pytest
from puzzle8.puzzle import GOAL_STATE
from puzzle8.ids import ids


def test_ids_already_solved() -> None:
    """IDS on the goal state returns a path of length 1 and 0 moves."""
    result = ids(GOAL_STATE)
    assert result is not None
    assert result.path == [GOAL_STATE]
    assert result.solution_length == 0


def test_ids_one_move() -> None:
    """IDS finds a 1-move solution."""
    start = (1, 2, 3, 4, 5, 6, 7, 0, 8)  # blank one step left of goal
    result = ids(start)
    assert result is not None
    assert result.path[0] == start
    assert result.path[-1] == GOAL_STATE
    assert result.solution_length == 1


def test_ids_solution_valid() -> None:
    """Every consecutive pair in the solution path is a valid move."""
    from puzzle8.puzzle import neighbors
    start = (1, 2, 3, 0, 4, 6, 7, 5, 8)
    result = ids(start)
    assert result is not None
    for a, b in zip(result.path, result.path[1:]):
        assert b in list(neighbors(a))


def test_ids_nodes_generated_positive() -> None:
    """nodes_generated is positive for non-trivial problems."""
    start = (1, 2, 3, 0, 4, 6, 7, 5, 8)
    result = ids(start)
    assert result is not None
    assert result.nodes_generated > 0
