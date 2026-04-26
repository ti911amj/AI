"""Board representation for the 8-Puzzle.

The board is represented as a tuple of 9 integers (0–8), where 0 is the blank tile.
Indices correspond to positions in row-major order:

    0 | 1 | 2
    ---------
    3 | 4 | 5
    ---------
    6 | 7 | 8
"""

from __future__ import annotations

import random
from typing import Iterator

# A board state is an immutable tuple of 9 integers.
Board = tuple[int, ...]

GOAL_STATE: Board = (1, 2, 3, 4, 5, 6, 7, 8, 0)
BOARD_SIZE = 3


def blank_index(board: Board) -> int:
    """Return the index of the blank tile (0) in *board*."""
    return board.index(0)


def neighbors(board: Board) -> Iterator[Board]:
    """Yield all boards reachable from *board* in one move.

    A move slides an adjacent tile into the blank position.

    Examples:
        >>> from puzzle8.puzzle import GOAL_STATE, neighbors
        >>> sorted(neighbors(GOAL_STATE))
        [(1, 2, 3, 4, 5, 0, 7, 8, 6), (1, 2, 3, 4, 5, 6, 7, 0, 8)]
    """
    idx = blank_index(board)
    row, col = divmod(idx, BOARD_SIZE)
    tiles = list(board)
 
    for delta, valid in ( # delta, valid move condition for each possible move direction
        (-BOARD_SIZE, row > 0),               # up
        (+BOARD_SIZE, row < BOARD_SIZE - 1),  # down
        (-1,          col > 0),               # left
        (+1,          col < BOARD_SIZE - 1),  # right
    ):
        if valid:
            neighbour = tiles[:] # Create a copy of the current board state to modify for the neighbor
            neighbour[idx], neighbour[idx + delta] = neighbour[idx + delta], neighbour[idx]
            yield tuple(neighbour)


def random_state(seed: int | None = None) -> Board:
    """Return a random, solvable 8-Puzzle board.

    Args:
        seed: Optional RNG seed for reproducibility.

    Returns:
        A solvable board chosen uniformly at random.
    """
    from puzzle8.parity import is_solvable  # local import avoids circular dependency

    rng = random.Random(seed)
    tiles = list(range(9))
    rng.shuffle(tiles)
    board: Board = tuple(tiles)
    if not is_solvable(board):
        # Swap any two non-blank tiles to flip parity
        non_blank = [idx for idx, t in enumerate(tiles) if t != 0]
        i, j = non_blank[0], non_blank[1]
        tiles[i], tiles[j] = tiles[j], tiles[i]
        board = tuple(tiles)
    return board
