import pressure_plate
import numpy as np
from collections import deque
import copy
from search_problem import PressurePlateProblem
from search import astar_search

# Map constants representing different cell types
BLANK = 0
WALL = 99
FLOOR = 98
AGENT = 1
GOAL = 2
AGENT_ON_GOAL = 3

# Deterministic transition probabilities (100% chance for the chosen direction)
forced_actions = {
    'U': [1, 0, 0, 0],
    'L': [0, 1, 0, 0],
    'R': [0, 0, 1, 0],
    'D': [0, 0, 0, 1]
}

class Controller:
    """This class is a controller for a pressure plate game using MDP and A*."""

    def __init__(self, game: pressure_plate.Game):
        """
        Initialize the controller, solve the base problem with A*, 
        and pre-calculate the value iteration policy.
        """
        self.original_game = game
        self.map = add_border(game.get_current_state()[0])
        
        # Use A* to find an initial deterministic path to the goal
        problem = PressurePlateProblem(self.map)
        result = astar_search(problem)
        self.solution_exist = False

        if result is None:
            solution = []
        else:
            self.solution_exist = True
            goal_node, expanded = result
            path = goal_node.path()[::-1]
            solution = [node.action for node in path][1:]

        # Adjust solution actions and create states along the optimal path
        swap_map = {'U': 'D', 'D': 'U'}
        new_solution = [swap_map.get(a, a) for a in solution]
        solution_states = self.create_solution_states(new_solution)
        
        # Build initial value and policy maps from the A* solution
        self.value_solution, self.policy_solution = self.create_solution_policy(new_solution, solution_states)
        
        # Identify goal coordinates for heuristic and reward calculations
        goal_pos = np.argwhere(self.map == pressure_plate.GOAL)
        self.goal_coords = (goal_pos[0][0], goal_pos[0][1])
        
        # Find reachable states within a certain horizon and run value iteration
        reachable_states = self.create_reachable_nodes(solution_states)
        self.V, self.policy = self.value_iteration(reachable_states=reachable_states)

    def create_solution_policy(self, solution_actions, solution_states):
        """
        Maps states on the optimal path to their respective actions and indices.
        """
        value_map = {}
        policy_map = {}
        
        # Map each state to its step index in the solution
        for i, game_state in enumerate(solution_states[:-1]):
            current_state = game_state.get_current_state()
            hashable_state = tuple(current_state[0].flatten())
            value_map[hashable_state] = i
            policy_map[hashable_state] = solution_actions[i]

        # Handle the final goal state
        final_state = solution_states[-1].get_current_state()
        hashable_final = tuple(final_state[0].flatten())
        value_map[hashable_final] = len(solution_states)
        policy_map[hashable_final] = "U"
        
        return value_map, policy_map
            
    def create_reachable_nodes(self, solution_states, horizon=4):
        """
        Performs a limited BFS to find all states reachable from the optimal path 
        within a specific number of steps.
        """
        reachable_nodes = []
        for base_state in solution_states:
            visited = set()
            queue = deque([(copy.deepcopy(base_state), 0)])
            
            while queue:
                current_game, depth = queue.popleft()
                if depth >= horizon:
                    break
                
                state_data = current_game.get_current_state()
                hashable_map = tuple(state_data[0].flatten())
                
                if hashable_map in visited:
                    continue
                
                visited.add(hashable_map)
                reachable_nodes.append(current_game)
                
                # Explore all possible directions
                for action in ["U", "L", "R", "D"]:
                    next_game = copy.deepcopy(current_game)
                    next_game._chosen_action_prob = forced_actions
                    next_game.submit_next_action(action)
                    queue.append((next_game, depth + 1))
                    
        return reachable_nodes
            
    def create_solution_states(self, solution_actions):
        """
        Executes the solution actions on a copy of the game to record 
        every intermediate state.
        """
        game_copy = copy.deepcopy(self.original_game)
        states_list = [copy.deepcopy(self.original_game)]
        game_copy._chosen_action_prob = forced_actions
        
        for action in solution_actions:
            game_copy.submit_next_action(action)
            states_list.append(copy.deepcopy(game_copy))
            
        # Identify which plates are pressed in the final solution state
        final_map = states_list[-1].get_current_state()[0]
        plates_pressed = [cell - 20 for row in final_map for cell in row if 30 <= cell < 40]
        self.opened_doors = plates_pressed
        
        return states_list
        
    def choose_next_action(self, state):
        """
        Determines the best action using the pre-calculated policy or falls 
        back to A* if a new solution is required.
        """
        hashable_state = tuple(state[0].flatten())

        # 1. Check if current state is in our pre-calculated solution path
        if hashable_state in self.policy_solution:
            return self.policy_solution[hashable_state]
        
        # 2. Check if state was found during Value Iteration
        if hashable_state in self.policy:
            return self.policy[hashable_state]
        
        # 3. Fallback: If no solution exists, move randomly
        if not self.solution_exist:
            return np.random.choice(["U", "R", "D", "L"])
        
        # 4. Recalculate A* if we are completely off-track
        problem = PressurePlateProblem(add_border(state[0]))
        result = astar_search(problem)
        
        if result is None:
            self.solution_exist = False
            return np.random.choice(["U", "R", "D", "L"])
        
        # Re-initialize path if A* finds a new way
        self.solution_exist = True
        goal_node, _ = result
        path = goal_node.path()[::-1]
        solution = [node.action for node in path][1:]
        
        swap_map = {'U': 'D', 'D': 'U'}
        new_solution = [swap_map.get(a, a) for a in solution]
        solution_states = self.create_solution_states(new_solution)
        self.value_solution, self.policy_solution = self.create_solution_policy(new_solution, solution_states)
        
        if hashable_state in self.policy_solution:
            return self.policy_solution[hashable_state]
        
        return np.random.choice(["U", "R", "D", "L"])

    def value_iteration(self, gamma=0.9, epochs=15, reachable_states=None):
        """
        Performs the Value Iteration algorithm to compute an optimal policy 
        for the reachable state space.
        """
        reachable = [game.get_current_state() for game in reachable_states]
        values = {}
        policy = {}
        
        # Initialize values using Manhattan distance to goal
        for state in reachable:
            hashable_state = tuple(state[0].flatten())
            values[hashable_state] = self.init_V(state)
            policy[hashable_state] = "U"
            
        for _ in range(epochs):
            new_values = {}
            for state in reachable:
                hashable_state = tuple(state[0].flatten())
                best_val = -np.inf
                best_act = "U"
                
                grid, agent_pos, steps, done, successful = state
                
                for action in ["U", "L", "R", "D"]:
                    expected_value = 0.0
                    
                    # Simulate outcomes based on transition probabilities
                    for i, real_action in enumerate(["U", "L", "R", "D"]):
                        # Setup a temporary game instance to calculate next state
                        temp_game = copy.deepcopy(self.original_game)
                        temp_game._agent_pos, temp_game._steps = agent_pos, steps
                        temp_game._done, temp_game._successful = done, successful
                        temp_game._map = grid.copy()
                        
                        prob = temp_game._chosen_action_prob[action][i]
                        if prob == 0: continue # Optimization
                        
                        temp_game._chosen_action_prob = forced_actions
                        temp_game.submit_next_action(real_action)
                        
                        next_state = temp_game.get_current_state()
                        hashable_next = tuple(next_state[0].flatten())
                        
                        v_next = values.get(hashable_next, 0)
                        reward = temp_game.get_current_reward() + self.get_custom_reward(next_state)
                        
                        expected_value += prob * (reward + gamma * v_next)
                    
                    if expected_value > best_val:
                        best_val = expected_value
                        best_act = action
                
                new_values[hashable_state] = best_val
                policy[hashable_state] = best_act
            values = new_values
            
        return values, policy

    def get_custom_reward(self, state):
        """
        Calculates additional rewards or penalties based on specific game conditions.
        """
        reward = 0
        hashable_state = tuple(state[0].flatten())
        
        # Reward for staying on the optimal A* path
        if hashable_state in self.policy_solution:
            reward += 100
            
        grid = state[0]
        # Penalty for being in tight spaces near objective doors
        for door_id in self.opened_doors:
            positions = np.argwhere(grid == door_id)
            for r, c in positions:
                walls = 0
                if r > 0 and grid[r-1, c] == 99: walls += 1
                if r < grid.shape[0]-1 and grid[r+1, c] == 99: walls += 1
                if c > 0 and grid[r, c-1] == 99: walls += 1
                if c < grid.shape[1]-1 and grid[r, c+1] == 99: walls += 1
                
                if walls >= 2:
                    reward -= 50
        return reward

    def init_V(self, state):
        """Initial value heuristic: Negative Manhattan distance to goal."""
        agent_pos = state[1]
        dist = abs(agent_pos[0] - self.goal_coords[0]) + abs(agent_pos[1] - self.goal_coords[1])
        return -dist

def add_border(arr, border_value=99):
    """Adds a surrounding border of walls to the game grid."""
    rows, cols = arr.shape
    bordered_arr = np.full((rows + 2, cols + 2), border_value, dtype=arr.dtype)
    bordered_arr[1:-1, 1:-1] = arr
    return bordered_arr