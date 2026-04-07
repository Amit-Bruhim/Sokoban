import ex1
import search
import time
import threading
import signal
import sys
sys.stdout.reconfigure(encoding='utf-8')


# Global variables for timeout tracking
timeout_occurred = False
timeout_problem = None
timeout_algorithm = None
timeout_duration = 5 * 60  # 5 minutes in seconds

def timeout_handler():
    """Handler for timeout signal"""
    global timeout_occurred, timeout_problem, timeout_algorithm
    timeout_occurred = True
    print(f"\n\n⚠️ TIMEOUT WARNING: 5 minutes have passed!")
    print(f"Last working on problem {timeout_problem} with {timeout_algorithm} algorithm")
    print("Continuing execution, but total time will exceed recommended limit...\n\n")

def set_timeout():
    """Set a timeout for 5 minutes"""
    timer = threading.Timer(timeout_duration, timeout_handler)
    timer.daemon = True
    timer.start()
    return timer

def run_problem(func, targs=(), kwargs=None):
    """Run a search function with given parameters and catch exceptions"""
    if kwargs is None:
        kwargs = {}
    result = (-3, "default")
    try:
        result = func(*targs, **kwargs)
    except Exception as e:
        result = (-3, e)
    return result

def get_solution_length(result):
    """Extract solution length from a search result"""
    if result and isinstance(result[0], search.Node):
        solve = result[0].path()[::-1]
        solution = [pi.action for pi in solve][1:]
        return len(solution), solution
    return None, None

def solve_problem(problem, algorithm, expected_length=None, optimal_length=None):
    """Solve a single problem with the specified algorithm and validate the result"""
    global timeout_problem, timeout_algorithm
    
    timeout_problem = problem_index
    timeout_algorithm = algorithm
    
    start_time = time.time()
    
    try:
        p = ex1.create_pressure_plate_problem(problem)
    except Exception as e:
        print(f"Error creating problem: {e}")
        return None, 0, None
    
    if algorithm == "gbfs":
        result = run_problem((lambda p: search.greedy_best_first_graph_search(p, p.h)), targs=[p])
    else:  # astar
        result = run_problem((lambda p: search.astar_search(p, p.h)), targs=[p])
    
    elapsed_time = time.time() - start_time
    
    solution_length, solution = get_solution_length(result)
    
    return solution_length, elapsed_time, solution

def print_problem(problem):
    """Print a problem's grid representation"""
    for row in problem:
        print(row)

# Dictionary of expected solution lengths for each problem
expected_solutions = {
    1: None,       # No solution
    2: None,       # No solution
    3: None,       # No solution
    4: 16,         # Solution length = 16
    5: None,       # No solution
    6: None,       # No solution
    7: 14,         # Solution length = 14
    8: None,       # No solution
    9: 34,         # Solution length = 34
    10: None,      # No solution
    11: 50,        # Solution length = 50
    12: 122,       # Solution length = 122
    13: 98,        # Solution length = 98
    14: 48,        # Solution length = 48
    15: 182        # Solution length = 182
}

# Test problems
problem1 = (
    (99, 99, 99, 99, 99),
    (99, 2, 99, 1, 99),
    (99, 98, 40, 98, 99),
    (99, 98, 20, 98, 99),
    (99, 99, 99, 99, 99),
)

problem2 = (
    (99, 99, 99, 99, 99),
    (99, 2, 99, 1, 99),
    (99, 98, 40, 98, 99),
    (99, 98, 10, 98, 99),
    (99, 99, 99, 99, 99),
)

problem3 = (
    (99, 99, 99, 99, 99, 99),
    (99, 98, 98, 98, 1, 99),
    (99, 98, 98, 10, 98, 99),
    (99, 99, 99, 98, 98, 99),
    (99, 2, 40, 20, 98, 99),
    (99, 99, 99, 99, 99, 99),
)

problem4 = (
    (99, 99, 99, 99, 99, 99),
    (99, 98, 98, 40, 2, 99),
    (99, 98, 10, 99, 99, 99),
    (99, 98, 98, 98, 98, 99),
    (99, 1, 98, 98, 20, 99),
    (99, 99, 99, 99, 99, 99),
)

problem5 = (
    (99, 99, 99, 99, 99, 99),
    (99, 2, 40, 98, 1, 99),
    (99, 99, 99, 98, 98, 99),
    (99, 20, 98, 10, 98, 99),
    (99, 20, 98, 11, 98, 99),
    (99, 99, 99, 99, 99, 99),
)

problem6 = (
    (99, 99, 99, 99, 99, 99),
    (99, 98, 98, 98, 1, 99),
    (99, 40, 99, 99, 99, 99),
    (99, 20, 99, 2, 10, 99),
    (99, 98, 98, 98, 98, 99),
    (99, 99, 99, 99, 99, 99),
)

problem7 = (
    (99, 99, 99, 99, 99, 99, 99, 99),
    (99, 2, 98, 98, 41, 98, 98, 99),
    (99, 98, 99, 99, 99, 98, 98, 99),
    (99, 98, 99, 98, 98, 11, 21, 99),
    (99, 40, 99, 98, 99, 99, 99, 99),
    (99, 98, 10, 98, 98, 98, 20, 99),
    (99, 98, 98, 98, 98, 98, 1, 99),
    (99, 99, 99, 99, 99, 99, 99, 99),
)

problem8 = (
    (99, 99, 99, 99, 99, 99, 99),
    (99, 98, 98, 98, 98, 1, 99),
    (99, 98, 98, 10, 98, 98, 99),
    (99, 20, 98, 98, 11, 98, 99),
    (99, 41, 99, 98, 98, 98, 99),
    (99, 2, 40, 21, 98, 98, 99),
    (99, 99, 99, 99, 99, 99, 99),
)

problem9 = (
    (99, 99, 99, 99, 99, 99, 99, 99, 99, 99),
    (99, 22, 98, 98, 98, 12, 98, 98, 1, 99),
    (99, 98, 98, 11, 98, 10, 98, 99, 98, 99),
    (99, 98, 98, 99, 42, 99, 99, 99, 98, 99),
    (99, 98, 99, 99, 98, 98, 98, 99, 40, 99),
    (99, 41, 99, 98, 98, 98, 21, 99, 98, 99),
    (99, 98, 99, 98, 98, 98, 20, 99, 98, 99),
    (99, 98, 99, 99, 99, 99, 99, 99, 98, 99),
    (99, 2, 98, 98, 98, 98, 98, 98, 98, 99),
    (99, 99, 99, 99, 99, 99, 99, 99, 99, 99),
)

problem10 = (
    (99, 99, 99, 99, 99, 99, 99, 99, 99, 99),
    (99, 2, 99, 29, 98, 98, 98, 98, 1, 99),
    (99, 98, 49, 98, 98, 98, 98, 16, 98, 99),
    (99, 99, 99, 99, 48, 99, 99, 47, 99, 99),
    (99, 98, 98, 98, 98, 99, 98, 98, 98, 99),
    (99, 27, 98, 98, 98, 99, 98, 98, 98, 99),
    (99, 98, 98, 19, 98, 99, 98, 98, 98, 99),
    (99, 28, 98, 98, 98, 46, 98, 18, 98, 99),
    (99, 98, 98, 98, 98, 99, 98, 26, 98, 99),
    (99, 99, 99, 99, 99, 99, 99, 99, 99, 99),
)

problem11 = (
    (99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99),
    (99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 98, 98, 98, 98, 99),
    (99, 99, 99, 98, 98, 99, 99, 99, 99, 99, 98, 99, 98, 98, 99),
    (99, 99, 98, 98, 98, 99, 99, 98, 25, 99, 98, 98, 99, 98, 99),
    (99, 99, 98, 98, 98, 98, 98, 98, 45, 98, 2, 98, 99, 98, 99),
    (99, 99, 99, 42, 99, 99, 99, 98, 98, 99, 99, 99, 99, 98, 99),
    (99, 99, 98, 98, 22, 99, 99, 99, 99, 99, 98, 98, 98, 98, 99),
    (99, 99, 98, 98, 98, 99, 98, 98, 98, 99, 98, 99, 99, 99, 99),
    (99, 99, 98, 98, 98, 99, 98, 98, 12, 99, 98, 98, 98, 98, 99),
    (99, 99, 99, 41, 99, 99, 98, 15, 98, 98, 23, 99, 99, 98, 99),
    (99, 98, 98, 98, 20, 99, 98, 98, 98, 98, 98, 99, 99, 98, 99),
    (99, 98, 10, 98, 98, 99, 98, 98, 99, 98, 98, 99, 99, 98, 99),
    (99, 98, 98, 98, 11, 40, 98, 98, 98, 13, 98, 99, 99, 98, 99),
    (99, 1, 98, 98, 21, 99, 98, 98, 98, 98, 98, 98, 43, 98, 99),
    (99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99),
)

problem12 = (
    (99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99),
    (99, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 99),  
    (99, 98, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 98, 99),
    (99, 98, 99, 21, 98, 99, 23, 98, 98, 98, 98, 98, 98, 98, 99),  
    (99, 98, 99, 98, 98, 43, 98, 98, 98, 13, 98, 98, 98, 98, 99),
    (99, 98, 99, 11, 98, 99, 98, 98, 10, 98, 98, 98, 98, 98, 99),  
    (99, 98, 99, 98, 98, 99, 98, 98, 98, 98, 98, 99, 99, 99, 99),
    (99, 1, 99, 99, 99, 99, 99, 99, 41, 99, 99, 99, 98, 2, 99),  
    (99, 98, 99, 98, 98, 98, 99, 98, 98, 98, 98, 99, 98, 98, 99),
    (99, 98, 99, 98, 98, 98, 99, 98, 98, 98, 14, 99, 98, 98, 99),  
    (99, 98, 99, 98, 98, 98, 99, 98, 98, 98, 98, 99, 98, 98, 99),
    (99, 98, 99, 20, 98, 98, 44, 98, 98, 98, 24, 99, 98, 98, 99),  
    (99, 98, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 40, 99),
    (99, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 99),               
    (99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99),
)

problem13 = (
    (99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99),
    (99, 98, 99, 99, 98, 98, 98, 98, 99, 99, 98, 98, 98, 98, 99),
    (99, 98, 98, 98, 98, 22, 99, 98, 99, 99, 98, 99, 99, 98, 99),
    (99, 98, 98, 99, 99, 99, 99, 98, 11, 98, 98, 99, 99, 98, 99),
    (99, 99, 98, 98, 12, 98, 99, 14, 99, 99, 98, 99, 99, 98, 99),
    (99, 99, 98, 98, 98, 98, 99, 98, 99, 99, 21, 99, 99, 98, 99),
    (99, 98, 98, 98, 98, 98, 99, 98, 98, 99, 99, 99, 99, 98, 99),
    (99, 98, 98, 98, 98, 99, 99, 98, 98, 99, 99, 99, 99, 98, 99),
    (99, 23, 98, 98, 99, 99, 99, 24, 98, 99, 99, 99, 99, 98, 99),
    (99, 99, 99, 98, 99, 99, 99, 99, 44, 99, 99, 99, 99, 98, 99),
    (99, 98, 98, 98, 99, 99, 99, 99, 98, 98, 98, 98, 98, 98, 99),
    (99, 98, 99, 98, 99, 99, 99, 99, 99, 99, 99, 99, 99, 98, 99),
    (99, 98, 99, 98, 99, 99, 99, 99, 99, 99, 99, 99, 99, 98, 99),
    (99, 98, 13, 98, 99, 99, 99, 99, 99, 99, 99, 99, 99, 98, 99),
    (99, 1, 98, 98, 99, 99, 99, 99, 99, 2, 43, 42, 41, 98, 99),
    (99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99),
)

problem14 = (
    (99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99),
    (99, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 2, 99),
    (99, 99, 99, 99, 99, 99, 99, 49, 99, 99, 99, 99, 99, 99, 99, 99, 98, 99, 99, 99),
    (99, 98, 98, 26, 99, 29, 98, 98, 27, 99, 98, 98, 98, 98, 99, 98, 98, 98, 98, 99),
    (99, 98, 98, 98, 99, 98, 98, 98, 98, 99, 98, 98, 18, 98, 99, 98, 98, 98, 98, 99),
    (99, 98, 98, 98, 46, 98, 98, 98, 98, 47, 98, 98, 98, 98, 48, 98, 98, 98, 98, 99),
    (99, 98, 98, 98, 99, 98, 98, 98, 98, 99, 98, 98, 98, 98, 99, 98, 98, 98, 98, 99),
    (99, 98, 98, 98, 99, 98, 98, 98, 17, 99, 98, 98, 98, 98, 99, 98, 98, 98, 98, 99),
    (99, 98, 98, 98, 99, 98, 98, 98, 98, 99, 98, 98, 98, 98, 99, 98, 98, 98, 98, 99),
    (99, 98, 98, 16, 99, 98, 98, 19, 98, 99, 98, 98, 98, 98, 99, 98, 98, 98, 98, 99),
    (99, 98, 98, 98, 99, 98, 98, 98, 98, 99, 28, 98, 98, 98, 99, 98, 98, 98, 98, 99),
    (99, 99, 42, 99, 99, 99, 43, 99, 99, 99, 99, 99, 44, 99, 99, 99, 99, 45, 99, 99),
    (99, 22, 98, 98, 98, 12, 98, 98, 98, 99, 98, 98, 98, 24, 98, 98, 98, 98, 98, 99),
    (99, 98, 98, 98, 13, 98, 98, 98, 23, 99, 98, 98, 98, 98, 98, 98, 98, 98, 25, 99),
    (99, 98, 98, 98, 98, 98, 98, 98, 98, 99, 98, 14, 98, 98, 98, 98, 98, 98, 98, 99),
    (99, 98, 98, 98, 98, 98, 98, 98, 98, 99, 98, 98, 98, 98, 98, 98, 98, 98, 98, 99),
    (99, 99, 99, 99, 40, 99, 99, 99, 99, 99, 99, 99, 99, 99, 41, 99, 99, 99, 99, 99),
    (99, 98, 98, 98, 98, 98, 98, 98, 98, 99, 21, 98, 98, 98, 98, 11, 98, 15, 98, 99),
    (99, 98, 98, 98, 98, 20, 10, 98, 98, 1, 98, 98, 98, 98, 98, 98, 98, 98, 98, 99),
    (99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99),
)

problem15 = (
    (99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99),
    (99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 98, 98, 98, 98, 23, 99, 98, 98, 98, 98, 99),
    (99, 99, 99, 99, 99, 99, 98, 98, 98, 99, 14, 98, 98, 98, 98, 99, 98, 98, 13, 98, 99),
    (99, 99, 99, 99, 99, 24, 98, 98, 98, 43, 98, 98, 98, 99, 99, 99, 98, 98, 99, 99, 99),
    (99, 99, 99, 99, 99, 98, 98, 15, 98, 99, 99, 98, 98, 99, 99, 99, 98, 98, 99, 99, 99),
    (99, 98, 98, 98, 99, 98, 98, 98, 98, 99, 99, 98, 98, 99, 99, 99, 98, 98, 99, 99, 99),
    (99, 25, 98, 98, 44, 98, 98, 98, 98, 99, 99, 98, 98, 98, 99, 99, 98, 98, 99, 99, 99),
    (99, 98, 98, 98, 99, 98, 98, 98, 98, 99, 99, 98, 98, 98, 99, 98, 11, 98, 99, 99, 99),
    (99, 98, 98, 98, 99, 99, 98, 98, 98, 99, 99, 98, 98, 98, 99, 98, 98, 98, 99, 99, 99),
    (99, 98, 98, 99, 99, 99, 99, 99, 99, 99, 98, 98, 99, 99, 99, 99, 98, 98, 99, 99, 99),
    (99, 99, 45, 99, 99, 99, 99, 99, 99, 99, 99, 41, 99, 99, 99, 99, 99, 42, 99, 99, 99),
    (99, 98, 98, 98, 99, 99, 99, 99, 99, 99, 98, 98, 99, 99, 99, 99, 98, 98, 98, 99, 99),
    (99, 98, 98, 98, 99, 99, 99, 99, 99, 99, 98, 98, 98, 98, 98, 12, 98, 98, 98, 99, 99),
    (99, 98, 16, 98, 98, 98, 98, 17, 27, 99, 22, 98, 98, 98, 98, 98, 98, 98, 21, 99, 99),
    (99, 98, 26, 98, 98, 98, 98, 16, 26, 99, 98, 98, 98, 98, 98, 98, 98, 98, 98, 99, 99),
    (99, 99, 99, 99, 99, 99, 46, 99, 99, 99, 99, 99, 99, 99, 40, 99, 99, 99, 99, 99, 99),
    (99, 99, 99, 99, 28, 18, 98, 99, 99, 99, 98, 10, 98, 98, 98, 98, 98, 98, 20, 99, 99),
    (99, 99, 99, 99, 29, 98, 98, 99, 99, 99, 98, 98, 98, 99, 99, 99, 99, 98, 98, 99, 99),
    (99, 99, 99, 99, 19, 98, 98, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 98, 99, 99),
    (99, 99, 99, 99, 98, 98, 98, 98, 98, 47, 48, 49, 98, 98, 98, 98, 2, 99, 1, 99, 99),
    (99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99),
)

def validate_astar_solution(solution_length, expected_length, problem_index, solution):
    """Validate A* algorithm solution against expected length"""
    print(f"A* solution length: {solution_length}")
    
    if expected_length is None:
        if solution_length is None:
            print("✅ PASSED: No solution found as expected")
            return True
        else:
            print(f"❌ FAILED: Found a solution with length {solution_length} but no solution was expected")
            return False
    else:
        if solution_length is None:
            print(f"❌ FAILED: No solution found but expected length {expected_length}")
            return False
        elif solution_length == expected_length:
            print(f"✅ PASSED: Optimal solution found ({solution_length} steps)")
            return True
        elif solution_length < expected_length:
            print(f"⚠️ BETTER SOLUTION FOUND: {solution_length} steps (expected: {expected_length})")
            print("Solution:", solution)
            print("Please notify Rotem to update the expected solution length!")
            return True
        else:
            print(f"❌ NOT OPTIMAL: Solution length {solution_length} is greater than expected {expected_length}")
            return False

def validate_gbfs_solution(solution_length, astar_length, problem_index, solution):
    """Validate GBFS algorithm solution against A* optimal solution"""
    print(f"GBFS solution length: {solution_length}")
    
    if astar_length is None:
        if solution_length is None:
            print("✅ PASSED: No solution found (matches A*)")
            return True
        else:
            print(f"⚠️ INTERESTING: GBFS found a solution ({solution_length} steps) but A* did not")
            print("This suggests a potential issue - please verify the solution carefully")
            return False
    else:
        if solution_length is None:
            print(f"❌ FAILED: No solution found but A* found one ({astar_length} steps)")
            return False
        elif solution_length == astar_length:
            print(f"✅ PASSED: Optimal solution found (matches A* with {astar_length} steps)")
            return True
        else:
            print(f"ℹ️ NOTE: Solution length {solution_length} differs from optimal A* solution ({astar_length} steps)")
            print(f"This is expected for GBFS which doesn't guarantee optimality")
            return True

def main():
    """Main function to run all tests and report results"""
    global problem_index
    
    # List all problems
    problems = [
        problem1, problem2, problem3, problem4, problem5, problem6, problem7,
        problem8, problem9, problem10, problem11, problem12, problem13, problem14, problem15
    ]
    
    # Set up timeout
    timer = set_timeout()
    
    # Track results
    results = {
        "astar": {"passed": 0, "failed": 0, "better": 0, "times": []},
        "gbfs": {"passed": 0, "failed": 0, "times": []}
    }
    
    # Track overall timing
    total_start_time = time.time()
    
    # Run tests for each problem
    for i, problem in enumerate(problems, 1):
        problem_index = i
        expected_length = expected_solutions[i]
        
        print(f"\n{'='*80}")
        print(f"Testing Problem {i}")
        print(f"{'='*80}")
        
        print("\nProblem grid:")
        print_problem(problem)
        
        # First run A* to get the optimal solution
        print(f"\nRunning A* algorithm...")
        astar_length, astar_time, astar_solution = solve_problem(problem, "astar", expected_length)
        results["astar"]["times"].append(astar_time)
        print(astar_solution)
        
        if validate_astar_solution(astar_length, expected_length, i, astar_solution):
            if astar_length is not None and expected_length is not None and astar_length < expected_length:
                results["astar"]["better"] += 1
            else:
                results["astar"]["passed"] += 1
        else:
            results["astar"]["failed"] += 1
        
        # Then run GBFS and compare with A*
        print(f"\nRunning GBFS algorithm...")
        gbfs_length, gbfs_time, gbfs_solution = solve_problem(problem, "gbfs", None, astar_length)
        results["gbfs"]["times"].append(gbfs_time)
        print(gbfs_solution)
        
        if validate_gbfs_solution(gbfs_length, astar_length, i, gbfs_solution):
            results["gbfs"]["passed"] += 1
        else:
            results["gbfs"]["failed"] += 1
        
        print(f"\nTime comparison: A*: {astar_time:.2f}s, GBFS: {gbfs_time:.2f}s")
        
        # Check if we've hit the timeout
        if timeout_occurred:
            print(f"\n⚠️ WARNING: Tests are taking too long (exceeding 5 minutes)")
    
    # Calculate total run time
    total_time = time.time() - total_start_time
    
    # Print summary report
    print("\n\n" + "="*100)
    print(f"TEST RESULTS SUMMARY".center(100))
    print("="*100)
    
    print(f"\nTotal execution time: {total_time:.2f} seconds")
    
    if total_time > timeout_duration:
        print(f"⚠️ WARNING: Total execution time exceeds 5 minutes limit ({timeout_duration} seconds)")
    
    print("\nA* Algorithm:")
    print(f"  ✅ Passed: {results['astar']['passed']}")
    print(f"  ❌ Failed: {results['astar']['failed']}")
    print(f"  ⚠️ Better solutions found: {results['astar']['better']}")
    print(f"  Average time per problem: {sum(results['astar']['times'])/len(problems):.2f} seconds")
    print(f"  Fastest problem: #{results['astar']['times'].index(min(results['astar']['times']))+1} ({min(results['astar']['times']):.2f}s)")
    print(f"  Slowest problem: #{results['astar']['times'].index(max(results['astar']['times']))+1} ({max(results['astar']['times']):.2f}s)")
    
    print("\nGBFS Algorithm:")
    print(f"  ✅ Passed: {results['gbfs']['passed']}")
    print(f"  ❌ Failed: {results['gbfs']['failed']}")
    print(f"  Average time per problem: {sum(results['gbfs']['times'])/len(problems):.2f} seconds")
    print(f"  Fastest problem: #{results['gbfs']['times'].index(min(results['gbfs']['times']))+1} ({min(results['gbfs']['times']):.2f}s)")
    print(f"  Slowest problem: #{results['gbfs']['times'].index(max(results['gbfs']['times']))+1} ({max(results['gbfs']['times']):.2f}s)")
    
    # Clean up timer
    timer.cancel()
    
    # Final status
    if results['astar']['failed'] > 0 or results['gbfs']['failed'] > 0:
        print("\n❌ SOME TESTS FAILED - Please check the detailed results above")
    elif timeout_occurred:
        print("\n⚠️ TESTS COMPLETED WITH TIMEOUT WARNING - Execution took too long")
    else:
        print("\n✅ ALL TESTS PASSED SUCCESSFULLY")

if __name__ == '__main__':
    main()