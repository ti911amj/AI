"""Utility functions for display and result formatting."""

from __future__ import annotations

from puzzle8.puzzle import Board, BOARD_SIZE


def board_to_str(board: Board) -> str:
    """Return a human-readable grid representation of *board*.

    Example output for the goal state::

        1 2 3
        4 5 6
        7 8 _

    The blank tile (0) is displayed as ``_``.

    Args:
        board: Board state to render.

    Returns:
        Multi-line string with rows separated by newlines.
    """
    rows = []
    for r in range(BOARD_SIZE):
        row = board[r * BOARD_SIZE:(r + 1) * BOARD_SIZE]
        rows.append(" ".join("_" if t == 0 else str(t) for t in row))
    return "\n".join(rows)


def print_board(board: Board) -> None:
    """Print *board* to stdout."""
    print(board_to_str(board))


def print_solution(path: list[Board] | None) -> None:
    """Print a solution path with step numbers and move count.

    If *path* is None, prints a message indicating no solution was found.

    Args:
        path: Sequence of boards from start to goal, or None.
    """
    if path is None:
        print("No solution found.")
        return
    for step, board in enumerate(path):
        print(f"Step {step}:")
        print_board(board)
    print(f"Solved in {len(path) - 1} moves.")


def format_result(
    algorithm: str,
    path: list[Board] | None,
    nodes_expanded: int,
) -> str:
    """Return a formatted summary string for a search result.

    Args:
        algorithm:      Name of the algorithm used (e.g. ``"A* (h2)"``).
        path:           Solution path, or None if unsolvable.
        nodes_expanded: Total nodes expanded during search.

    Returns:
        Single-line summary, e.g.
        ``"A* (h2): 12 moves, 340 nodes generated"``.
    """
    if path is None:
        return f"{algorithm}: no solution, {nodes_expanded} nodes generated"
    return f"{algorithm}: {len(path) - 1} moves, {nodes_expanded} nodes generated"
