import pressure_plate
import mdp_env_solver

def solve(game: pressure_plate.Game):
    """
    Executes the game using the MDP controller and displays the final results.
    """
    # Initialize the MDP policy controller
    policy = mdp_env_solver.Controller(game)
    
    # Main game loop
    for i in range(game.get_max_steps()):
        current_state = game.get_current_state()
        
        # Select and submit the next action based on the calculated policy
        action = policy.choose_next_action(current_state)
        game.submit_next_action(chosen_action=action)
        
        # Check if the game is done (game.get_current_state()[3] is the 'done' flag)
        if game.get_current_state()[3]:
            break

    # Extract final state details
    final_state = game.get_current_state()
    final_grid = final_state[0]
    steps_taken = final_state[2]
    is_successful = final_state[-1]

    # --- Print Results Section ---
    print("\n" + "="*20)
    print("  GAME RESULTS")
    print("="*20)
    
    print("Final Map State:")
    # Using .tolist() on the whole grid converts all np.int64 elements to standard Python ints
    clean_grid = final_grid.tolist()
    for row in clean_grid:
        # Formatting each cell to take 2 spaces for a perfectly aligned grid
        print("  " + " ".join(f"{cell:2}" for cell in row))
        
    print(f"\nFinished in: {steps_taken} steps")
    print(f"Total Reward: {game.get_current_reward()}")
    
    status = "SUCCESSFULLY" if is_successful else "UNSUCCESSFULLY"
    print(f"Game finished {status}.")
    print("="*20 + "\n")

    # Show visual history and return total reward
    game.show_history()
    return game.get_current_reward()

# Configuration for the MDP environment
example_config = {
    'chosen_action_prob': {
        'U': [0.9, 0.05, 0.05, 0], 
        'L': [0.1, 0.8, 0.075, 0.025],
        'R': [0.05, 0.05, 0.85, 0.05], 
        'D': [0.05, 0.1, 0.15, 0.7]
    },
    'finished_reward': 350,
    'opening_door_reward': {10: 5, 11: 7, 12: 9, 13: 11, 14: 13, 15: 15, 16: 17, 17: 19, 18: 21, 19: 23},
    'step_punishment': -2,
    'seed': 42
}

# Grid layout: 99=Wall, 2=Goal, 40=Locked Door, 10=Key, 20=Plate, 1=Agent
problem_grid = (
    (99, 99, 99, 99, 99, 99),
    (99, 2,  40, 98, 98, 99),
    (99, 99, 99, 10, 98, 99),
    (99, 98, 98, 98, 98, 99),
    (99, 20, 98, 98, 1,  99),
    (99, 99, 99, 99, 99, 99),
)

def main():
    """
    Main entry point to create and solve a specific game instance.
    """
    debug_mode = True
    # Initializing the game with max 100 steps
    game_instance = pressure_plate.create_pressure_plate_game((100, problem_grid, example_config, debug_mode))
    solve(game_instance)

if __name__ == "__main__":
    main()