"""Tests for astar.py — A* search."""

import pytest
from puzzle8.puzzle import GOAL_STATE
from puzzle8.heuristics import h1, h2
from puzzle8.astar import astar


@pytest.mark.parametrize("heuristic", [h1, h2])
def test_astar_already_solved(heuristic) -> None:
    result = astar(GOAL_STATE, heuristic)
    assert result is not None
    assert result.path == [GOAL_STATE]


@pytest.mark.parametrize("heuristic", [h1, h2])
def test_astar_one_move(heuristic) -> None:
    start = (1, 2, 3, 4, 5, 6, 7, 0, 8)
    result = astar(start, heuristic)
    assert result is not None
    assert result.path[0] == start
    assert result.path[-1] == GOAL_STATE
    assert result.solution_length == 1


def test_astar_h2_optimal() -> None:
    """A* with h2 finds a path no longer than A* with h1 (h2 dominates h1)."""
    start = (1, 2, 3, 0, 4, 6, 7, 5, 8)
    result_h1 = astar(start, h1)
    result_h2 = astar(start, h2)
    assert result_h1 is not None
    assert result_h2 is not None
    assert result_h2.solution_length <= result_h1.solution_length


def test_astar_nodes_generated_h2_less_than_h1() -> None:
    """A* with h2 expands fewer nodes than with h1 (h2 dominates h1)."""
    start = (1, 2, 3, 0, 4, 6, 7, 5, 8)
    result_h1 = astar(start, h1)
    result_h2 = astar(start, h2)
    assert result_h1 is not None
    assert result_h2 is not None
    assert result_h2.nodes_generated <= result_h1.nodes_generated
