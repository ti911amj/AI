"""A* search for the 8-Puzzle."""

from __future__ import annotations

import heapq
from typing import Callable

from puzzle8.puzzle import Board, GOAL_STATE, neighbors
from puzzle8.heuristics import h1, h2  # noqa: F401  (re-exported for callers)
from puzzle8.ids import SearchResult


def astar(
    start: Board,
    heuristic: Callable[[Board], int],
    goal: Board = GOAL_STATE,
) -> SearchResult | None:
    """Find an optimal solution path using A* search.

    Expands nodes in order of f(n) = g(n) + h(n), where g(n) is the cost
    from the start and h(n) is the admissible heuristic estimate to the goal.

    When called with h2 (Manhattan distance), the search is guaranteed to be
    optimal: h2 is admissible (never overestimates) and monotone/consistent
    (h(n) <= c(n,n') + h(n') for every successor n').  Consistency implies
    that the f-values along any path are non-decreasing, so A* never needs to
    reopen a closed node — the first time a node is expanded it is reached via
    an optimal path and can be permanently discarded afterwards.

    Args:
        start:     Initial board state.
        heuristic: Admissible heuristic function h(board) -> int.
        goal:      Target board state (defaults to GOAL_STATE).

    Returns:
        Shortest list of boards from *start* to *goal* (inclusive), or None
        if no solution exists.
    """
    # heap entries: (f, g, board, path)
    heap: list[tuple[int, int, Board, list[Board]]] = [] # Initialize an empty heap to store nodes to explore, with entries containing f, g, board state, and the path taken to reach that state
    heapq.heappush(heap, (heuristic(start), 0, start, [start])) # Push the initial state onto the heap with f = h(start) and g = 0

    closed: set[Board] = set() # Set to keep track of already expanded nodes to avoid re-expansion
    nodes_generated = 0

    while heap:
        f, g, board, path = heapq.heappop(heap)

        if board in closed:
            continue
        closed.add(board)

        if board == goal:
            return SearchResult(
                path=path,
                nodes_generated=nodes_generated,
                solution_length=len(path) - 1,
            )

        for neighbour in neighbors(board):
            if neighbour not in closed:
                new_g = g + 1
                new_f = new_g + heuristic(neighbour)
                heapq.heappush(heap, (new_f, new_g, neighbour, path + [neighbour]))
                nodes_generated += 1

    return None
