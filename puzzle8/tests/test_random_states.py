"""Test search methods on randomly generated solvable start states.

This script demonstrates question (b):
"Test your search methods for randomly generated start states. 
Remember to consider the parity considerations in Exercise 1."

The key insight: Only solvable states (even inversion parity) can reach the goal.
"""

import sys
sys.path.insert(0, 'src')

from puzzle8.puzzle import random_state, GOAL_STATE
from puzzle8.parity import is_solvable, count_inversions
from puzzle8.ids import ids
from puzzle8.astar import astar
from puzzle8.heuristics import h1, h2
from puzzle8.utils import print_board


def test_random_states(num_states: int = 5) -> None:
    """Generate random start states and test both search algorithms.
    
    Demonstrates that:
    1. Random states are generated with proper parity (solvable)
    2. Both IDS and A* find solutions for these states
    3. A* is more efficient than IDS
    """
    print(f"\n{'='*70}") # Print a header for the test
    print(f"Testing {num_states} Random Solvable Start States")
    print(f"{'='*70}\n")
    
    results = {
        'ids_moves': [],
        'ids_nodes': [],
        'astar_h1_moves': [],
        'astar_h1_nodes': [],
        'astar_h2_moves': [],
        'astar_h2_nodes': [],
    }
    
    for trial in range(num_states):
        print(f"\n{'─'*70}")
        print(f"Trial {trial + 1}: Random Generated Start State")
        print(f"{'─'*70}")
        
        # Generate a random solvable state
        start = random_state(seed=trial) # Generate a random state using a fixed seed for reproducibility
        inversions = count_inversions(start) # Count the number of inversions in the generated state to check parity
        
        print(f"\nStart state:")
        print_board(start)
        print(f"\nSolvability check (Exercise 1):")
        print(f"  Inversions: {inversions}")
        print(f"  Even (solvable): {inversions % 2 == 0} ✓")
        print(f"  is_solvable(): {is_solvable(start)} ✓")
        
        # Run IDS
        print(f"\n1. Iterative Deepening Search (IDS):")
        ids_result = ids(start) 
        if ids_result:
            print(f"   ✓ Solution found!")
            print(f"   - Moves: {ids_result.solution_length}")
            print(f"   - Nodes explored: {ids_result.nodes_generated}")
            results['ids_moves'].append(ids_result.solution_length)
            results['ids_nodes'].append(ids_result.nodes_generated)
        else:
            print(f"   ✗ No solution found (this should NOT happen for solvable states!)")
        
        # Run A* with h1
        print(f"\n2. A* Search with h1 (Misplaced Tiles):")
        astar_h1 = astar(start, h1)
        if astar_h1:
            print(f"   ✓ Solution found!")
            print(f"   - Moves: {astar_h1.solution_length}")
            print(f"   - Nodes explored: {astar_h1.nodes_generated}")
            results['astar_h1_moves'].append(astar_h1.solution_length)
            results['astar_h1_nodes'].append(astar_h1.nodes_generated)
        else:
            print(f"   ✗ No solution found (this should NOT happen for solvable states!)")
        
        # Run A* with h2
        print(f"\n3. A* Search with h2 (Manhattan Distance):")
        astar_h2 = astar(start, h2)
        if astar_h2:
            print(f"   ✓ Solution found!")
            print(f"   - Moves: {astar_h2.solution_length}")
            print(f"   - Nodes explored: {astar_h2.nodes_generated}")
            results['astar_h2_moves'].append(astar_h2.solution_length)
            results['astar_h2_nodes'].append(astar_h2.nodes_generated)
        else:
            print(f"   ✗ No solution found (this should NOT happen for solvable states!)")
        
        # Verify all found the same solution length (optimality)
        if ids_result and astar_h1 and astar_h2:
            moves_match = (
                ids_result.solution_length == astar_h1.solution_length == astar_h2.solution_length
            )
            print(f"\nOptimality check:")
            print(f"  All algorithms found {ids_result.solution_length}-move solution: {moves_match} ✓")
    
    # Summary statistics
    print(f"\n\n{'='*70}")
    print(f"SUMMARY: {num_states} Random States")
    print(f"{'='*70}\n")
    
    if results['ids_moves']:
        print(f"IDS:")
        print(f"  Avg moves: {sum(results['ids_moves']) / len(results['ids_moves']):.1f}")
        print(f"  Avg nodes: {sum(results['ids_nodes']) / len(results['ids_nodes']):.0f}")
    
    if results['astar_h1_moves']:
        print(f"\nA* (h1):")
        print(f"  Avg moves: {sum(results['astar_h1_moves']) / len(results['astar_h1_moves']):.1f}")
        print(f"  Avg nodes: {sum(results['astar_h1_nodes']) / len(results['astar_h1_nodes']):.0f}")
    
    if results['astar_h2_moves']:
        print(f"\nA* (h2):")
        print(f"  Avg moves: {sum(results['astar_h2_moves']) / len(results['astar_h2_moves']):.1f}")
        print(f"  Avg nodes: {sum(results['astar_h2_nodes']) / len(results['astar_h2_nodes']):.0f}")
    
    # Efficiency comparison
    if results['ids_nodes'] and results['astar_h2_nodes']:
        avg_ids = sum(results['ids_nodes']) / len(results['ids_nodes'])
        avg_h2 = sum(results['astar_h2_nodes']) / len(results['astar_h2_nodes'])
        speedup = avg_ids / avg_h2 if avg_h2 > 0 else 0
        print(f"\nEfficiency:")
        print(f"  A* (h2) is {speedup:.1f}x faster than IDS")
        print(f"  (explores {speedup:.1f}x fewer nodes on average)\n")


if __name__ == "__main__":
    # Test on 5 random states
    test_random_states(num_states=5)
