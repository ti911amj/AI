"""Iterative Deepening Search (IDS) for the 8-Puzzle."""

from __future__ import annotations

from dataclasses import dataclass 
from enum import Enum, auto 
from typing import Union 

from puzzle8.puzzle import Board, GOAL_STATE, neighbors


class _Sentinel(Enum): # Sentinel values for DFS results. 
    CUTOFF = auto()
    FAILURE = auto()


_CUTOFF = _Sentinel.CUTOFF
_FAILURE = _Sentinel.FAILURE

# Return type of the recursive helper: either a solution path or a sentinel.
_DFSResult = Union[list[Board], _Sentinel]


@dataclass
class SearchResult:
    """Result returned by :func:`ids`."""

    path: list[Board]
    nodes_generated: int
    solution_length: int


def ids(
    start: Board,
    goal: Board = GOAL_STATE,
) -> SearchResult | None:
    """Find a solution path using Iterative Deepening Search.

    Runs depth-limited DFS with depth limits 1, 2, 3, … until a solution is
    found.  Node counts are accumulated across all iterations.

    Args:
        start: Initial board state.
        goal:  Target board state (defaults to GOAL_STATE).

    Returns:
        :class:`SearchResult` on success, or ``None`` if the puzzle has no
        solution (the entire reachable state space was exhausted without
        finding the goal).
    """
    total_nodes = 0

    for depth in range(1, 10_000):  # effectively unbounded for the 8-puzzle
        counter: list[int] = [0]
        result = _depth_limited_search(goal, depth, [start], counter)
        total_nodes += counter[0]

        if result is _CUTOFF:
            continue
        if result is _FAILURE:
            return None  # puzzle is unsolvable
        # result is a solution path
        path: list[Board] = result  # type: ignore[assignment]
        return SearchResult(
            path=path,
            nodes_generated=total_nodes,
            solution_length=len(path) - 1,
        )

    return None  # exceeded depth bound (should not happen for valid inputs)


def _depth_limited_search(
    goal: Board,
    limit: int,
    path: list[Board],
    counter: list[int],
) -> _DFSResult:
    """Recursive depth-limited DFS — mirrors the lecture pseudocode exactly.

    Args:
        goal:    Target board state.
        limit:   Remaining depth budget.
        path:    Boards on the current path, *including* the current node at
                 ``path[-1]``.  Used for cycle detection.
        counter: Single-element list used as a mutable node counter.
                 Incremented each time a child is added to the path.

    Returns:
        A solution path (list of boards) when the goal is reached, or one of
        the sentinel values :data:`_CUTOFF` / :data:`_FAILURE`.
    """
    node = path[-1]

    if node == goal:
        return list(path)

    if limit == 0:
        return _CUTOFF

    cutoff_occurred = False

    for child in neighbors(node):
        if child in path:
            continue

        counter[0] += 1   # child generated
        path.append(child)

        result = _depth_limited_search(goal, limit - 1, path, counter)

        if result is not _CUTOFF and result is not _FAILURE:
            return result  # solution found — propagate upward
        if result is _CUTOFF:
            cutoff_occurred = True

        path.pop()

    return _CUTOFF if cutoff_occurred else _FAILURE
