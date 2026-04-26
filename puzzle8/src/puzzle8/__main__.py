"""Entry point: runs demo scenarios for the 8-Puzzle solver.

Usage:
    uv run python -m puzzle8
    # or, after installing:
    puzzle8
"""

from __future__ import annotations

from puzzle8.puzzle import GOAL_STATE
from puzzle8.parity import is_solvable
from puzzle8.heuristics import h1, h2
from puzzle8.ids import ids
from puzzle8.astar import astar
from puzzle8.utils import print_board, print_solution, format_result

_ABB1 = (7, 2, 4, 5, 0, 6, 8, 3, 1)


def demo_parity() -> None:
    """Demonstrate parity checking on a few boards."""
    print("=== Parity Check ===")
    boards = [
        ("Goal state",      GOAL_STATE),
        ("Abb. 1 start",    _ABB1), # The start state from the assignment, which is known to be solvable
        ("Unsolvable",      (1, 2, 3, 4, 5, 6, 8, 7, 0)),
    ]
    for label, board in boards:
        print_board(board)
        print(f"{label}: solvable = {is_solvable(board)}\n")


def demo_ids() -> None:
    """Demonstrate IDS on the Abb. 1 start state."""
    print("\n=== Iterative Deepening Search ===")
    result = ids(_ABB1)
    print(format_result("IDS", result.path if result else None,
                         result.nodes_generated if result else 0))
    print_solution(result.path if result else None)


def demo_astar() -> None:
    """Demonstrate A* with both heuristics on the Abb. 1 start state."""
    print("\n=== A* Search ===")
    result_h1 = astar(_ABB1, h1)
    result_h2 = astar(_ABB1, h2)
    print(format_result("A* (h1)", result_h1.path if result_h1 else None,
                         result_h1.nodes_generated if result_h1 else 0))
    print(format_result("A* (h2)", result_h2.path if result_h2 else None,
                         result_h2.nodes_generated if result_h2 else 0))
    if result_h1 and result_h2:
        print(f"h2 generated {result_h1.nodes_generated - result_h2.nodes_generated} fewer nodes than h1.")


def main() -> None:
    """Run all demo scenarios."""
    demo_parity()
    demo_ids()
    demo_astar()


if __name__ == "__main__":
    main()
