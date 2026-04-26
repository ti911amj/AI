"""Heuristic functions for 8-Puzzle search.

Both heuristics are admissible (never overestimate the true cost) and are
therefore suitable for A* search.
"""

from __future__ import annotations

from puzzle8.puzzle import Board, GOAL_STATE, BOARD_SIZE

# Precomputed goal position for each tile value (excluding blank).
# Maps tile → (row, col) based on GOAL_STATE.
_GOAL_POS: dict[int, tuple[int, int]] = {
    tile: (idx // BOARD_SIZE, idx % BOARD_SIZE) # Calculate row and column from index
    for idx, tile in enumerate(GOAL_STATE) # Iterate through GOAL_STATE to build the mapping
    if tile != 0
}


def h1(board: Board) -> int:
    """Count misplaced tiles (excluding the blank).

    A tile is misplaced when it is not in the position it occupies in
    GOAL_STATE.

    Args:
        board: Current board state.

    Returns:
        Number of tiles not in their goal position.

    Examples:
        >>> h1((7, 2, 4, 5, 0, 6, 8, 3, 1))
        8 
        >>> h1(GOAL_STATE)
        0
    """
    return sum(
        1 # Count 1 for each tile that is not in its goal position
        for idx, tile in enumerate(board) 
        if tile != 0 and tile != GOAL_STATE[idx] # Check if the tile is not blank and not in the correct position
    )


def h2(board: Board) -> int:
    """Sum of Manhattan distances of each tile to its goal position.

    The Manhattan distance for a tile is |row_current - row_goal| +
    |col_current - col_goal|.  The blank tile is excluded.

    Args:
        board: Current board state.

    Returns:
        Total Manhattan distance across all non-blank tiles.

    Examples:
        >>> h2((7, 2, 4, 5, 0, 6, 8, 3, 1))
        18 # Each tile's distance to its goal position is summed up
        >>> h2(GOAL_STATE)
        0
    """
    total = 0
    for idx, tile in enumerate(board):
        if tile != 0:
            r, c = divmod(idx, BOARD_SIZE)
            gr, gc = _GOAL_POS[tile]
            total += abs(r - gr) + abs(c - gc)
    return total
