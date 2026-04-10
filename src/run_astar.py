import os
import sys
import search_problem
import search
from simulation import run_simulation

# Suppress pygame welcome message and python warnings
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

def solve_and_simulate(problem_map):
    """
    Solves the grid problem using A* search and launches a visual simulation.
    """
    # Initialize the problem instance
    problem = search_problem.create_pressure_plate_problem(problem_map)

    print("Calculating path using A* algorithm...")
    
    # Execute A* search
    result = search.astar_search(problem, problem.h)

    # Check if result is a tuple (Node, cost) or just a Node
    if result:
        if isinstance(result, tuple):
            result_node = result[0]  # Extract the Node from the tuple
        else:
            result_node = result

        # Extract the sequence of actions
        path_nodes = result_node.path()
        solution_actions = [node.action for node in path_nodes[::-1] if node.action is not None]
        
        print(f"Solution found with {len(solution_actions)} steps!")
        print("Launching simulation...")
        
        run_simulation(problem_map, solution_actions)
    else:
        print("No solution found.")
        
def main():
    target_problem = (
        (99, 99, 99, 99, 99, 99, 99, 99, 99, 99),
        (99, 1, 98, 98, 99, 98, 10, 20, 99, 99),
        (99, 98, 99, 98, 98, 98, 99, 99, 99, 99),
        (99, 98, 98, 40, 99, 98, 98, 98, 98, 99),
        (99, 99, 99, 98, 99, 99, 99, 99, 98, 99),
        (99, 98, 98, 98, 99, 98, 42, 98, 98, 99),
        (99, 12, 99, 99, 99, 98, 99, 99, 99, 99),
        (99, 22, 99, 21, 11, 98, 98, 41, 99, 99),
        (99, 99, 99, 99, 99, 99, 99, 98, 2, 99),
        (99, 99, 99, 99, 99, 99, 99, 99, 99, 99)
    )

    solve_and_simulate(target_problem)

if __name__ == '__main__':
    main()