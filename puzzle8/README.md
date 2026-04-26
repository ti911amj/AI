# 8-Puzzle Solver

University assignment implementing AI search algorithms for the 8-Puzzle problem.

## Algorithms

| Algorithm | Module | Description |
|-----------|--------|-------------|
| IDS | `ids.py` | Iterative Deepening Search |
| A\* (h1) | `astar.py` + `heuristics.py` | A\* with misplaced-tile heuristic |
| A\* (h2) | `astar.py` + `heuristics.py` | A\* with Manhattan distance heuristic |

## Project Structure

```
8-puzzle-solver/
├── src/
│   └── puzzle8/
│       ├── __init__.py
│       ├── __main__.py     # demo entry point
│       ├── puzzle.py       # board representation, neighbors, random state
│       ├── parity.py       # solvability check (Aufgabe 1)
│       ├── heuristics.py   # h1 (misplaced tiles), h2 (Manhattan distance)
│       ├── ids.py          # Iterative Deepening Search
│       ├── astar.py        # A* search
│       └── utils.py        # pretty printing, result formatting
├── tests/
│   ├── test_puzzle.py
│   ├── test_parity.py
│   ├── test_heuristics.py
│   ├── test_ids.py
│   └── test_astar.py
├── main.py
├── pyproject.toml
└── README.md
```

## Setup

Requires [uv](https://docs.astral.sh/uv/).

```bash
# Install dependencies (including dev tools)
uv sync --dev

# Run demo
uv run python main.py
# or
uv run python -m puzzle8

# Run tests
uv run pytest

# Run tests with verbose output
uv run pytest -v
```

## Board Representation

The board is a tuple of 9 integers (0–8), where `0` is the blank tile.
Positions are in row-major order:

```
0 | 1 | 2
---------
3 | 4 | 5
---------
6 | 7 | 8
```

Goal state: `(1, 2, 3, 4, 5, 6, 7, 8, 0)`
