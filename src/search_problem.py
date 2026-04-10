import search

# Map constants
BLANK = 0
WALL = 99
FLOOR = 98
AGENT = 1
GOAL = 2
AGENT_ON_GOAL = 3
LOCKED_DOORS = list(range(40, 50))
PRESSED_PLATES = list(range(30, 40))
PRESSURE_PLATES = list(range(20, 30))
KEY_BLOCKS = list(range(10, 20))

# Movement directions
directions = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1)
}

class PressurePlateProblem(search.Problem):
    """
    This class implements the Pressure Plate puzzle as a search problem.
    The state is represented as: (agent_pos, key_blocks, pressure_plates, locked_doors, g)
    """

    def __init__(self, initial):
        self.map = initial
        self.goal = self.find_goal(initial)
        self.visited_states = set()
        
        # Extract initial positions of all dynamic elements
        agent = self.find_agent(initial)
        key_blocks = self.find_key_blocks(initial)
        pressure_plates = self.find_pressure_plates(initial)
        locked_doors = self.find_locked_doors(initial)
        
        initial_state = (agent, key_blocks, pressure_plates, locked_doors, 0)
        search.Problem.__init__(self, initial_state, self.goal)

    def successor(self, state):
        """
        Generates all valid successor states for the current state.
        Returns a list of (action, next_state) pairs.
        """
        successors = []
        for direction in directions:
            is_valid, new_state = self.make_move(state, direction)
            if is_valid:
                # Use canonical state to avoid redundant cycles in the search
                state_key = self.canonical_state(new_state)
                if state_key not in self.visited_states:
                    self.visited_states.add(state_key)
                    successors.append((direction, new_state))
        return successors

    def goal_test(self, state):
        """ Checks if the agent has reached the goal coordinates """
        agent_pos = state[0]
        return agent_pos == self.goal
            
    def h(self, node):
        """
        Heuristic function: Estimates the cost to reach the goal.
        Considers Manhattan distance, key-to-plate distances, and penalties.
        """
        agent, key_blocks, plates, doors, g = node.state  
        
        # 1. Penalty for remaining locked doors
        locked_doors_penalty = len(doors)
        
        # 2. Distance from keys to their corresponding pressure plates
        key_plate_distances = 0
        for kr, kc, k_type in key_blocks:
            min_dist = float('inf')
            for pr, pc, p_type in plates:
                if self.same_type(k_type, p_type):
                    dist = abs(pr - kr) + abs(pc - kc)
                    if dist < min_dist:
                        min_dist = dist

            key_plate_distances += 30 if min_dist == float('inf') else min_dist

        # 3. Penalty for keys stuck in corners (Deadlocks)
        corner_penalty = 0
        for kr, kc, _ in key_blocks:
            walls = 0
            for dr, dc in directions.values():
                if self.map[kr + dr][kc + dc] == WALL:
                    walls += 1
            if walls >= 2:
                corner_penalty = 5
                break
        
        # 4. Agent's Manhattan distance to the goal
        dist_to_goal = abs(agent[0] - self.goal[0]) + abs(agent[1] - self.goal[1])
        
        # Final weighted heuristic calculation
        h_val = (2 * dist_to_goal + 
                 1.8 * key_plate_distances + 
                 corner_penalty + 
                 locked_doors_penalty + 
                 1.5 * g)
        
        return 10 * h_val

    def canonical_state(self, state):
        """ Returns a sorted, hashable representation of the state for comparison """
        agent, keys, plates, doors, _ = state
        return (agent, tuple(sorted(keys)), tuple(sorted(plates)), tuple(sorted(doors)))

    def find_key_blocks(self, grid): 
        keys = [(r, c, val) for r, row in enumerate(grid) 
                for c, val in enumerate(row) if val in KEY_BLOCKS]
        return frozenset(keys)

    def find_locked_doors(self, grid):
        doors = [(r, c, val) for r, row in enumerate(grid) 
                 for c, val in enumerate(row) if val in LOCKED_DOORS]
        return frozenset(doors)

    def find_pressure_plates(self, grid):
        plates = [(r, c, val) for r, row in enumerate(grid) 
                  for c, val in enumerate(row) if val in PRESSURE_PLATES]
        return frozenset(plates)

    def make_move(self, state, action):
        """
        Logic for moving the agent and interacting with objects (keys, plates, doors).
        Returns (is_valid, new_state).
        """
        agent_pos, keys, plates, doors, g = state   
        dr, dc = directions[action]
        new_r, new_c = agent_pos[0] + dr, agent_pos[1] + dc
        new_pos = (new_r, new_c)

        # Check if agent is trying to push a key block
        for k_pos in keys:
            if k_pos[0] == new_r and k_pos[1] == new_c:
                push_r, push_c = new_r + dr, new_c + dc
                push_pos = (push_r, push_c)

                # Cannot push key into another key or a locked door
                if any(k[0] == push_r and k[1] == push_c for k in keys): return False, state
                if any(d[0] == push_r and d[1] == push_c for d in doors): return False, state

                # Check if pushing key onto a pressure plate
                for p_pos in plates:
                    if p_pos[0] == push_r and p_pos[1] == push_c:
                        if not self.same_type(k_pos[2], p_pos[2]):
                            return False, state # Wrong key type
                        
                        # Correct key on plate: Remove both and check for door opening
                        updated_plates = frozenset(plates - {p_pos})
                        updated_keys = frozenset(keys - {k_pos})
                        updated_doors = doors
                        
                        # If no more plates of this type remain, open corresponding doors
                        remaining = any(self.same_type(p[2], p_pos[2]) for p in updated_plates)
                        if not remaining:
                            updated_doors = frozenset({d for d in doors if not self.same_type(d[2], p_pos[2])})
                                    
                        return True, (new_pos, updated_keys, updated_plates, updated_doors, g + 1)

                # Standard floor push
                target_val = self.map[push_r][push_c]
                if target_val == WALL or target_val == GOAL or target_val in PRESSURE_PLATES:
                    return False, state
                
                updated_keys = frozenset((keys - {k_pos}) | {(push_r, push_c, k_pos[2])})
                return True, (new_pos, updated_keys, plates, doors, g + 1)

        # Agent movement constraints (Walls, Locked Doors, or Pressure Plates)
        if any(d[0] == new_r and d[1] == new_c for d in doors): return False, state
        if any(p[0] == new_r and p[1] == new_c for p in plates): return False, state
        
        if self.map[new_r][new_c] == WALL:
            return False, state
        
        return True, (new_pos, keys, plates, doors, g + 1)
            
    def same_type(self, val1, val2):
        """ Checks if two IDs belong to the same object family (e.g., Key 11 and Door 41) """
        return val1 % 10 == val2 % 10

    def find_goal(self, grid):
        for r, row in enumerate(grid):
            for c, val in enumerate(row):
                if val == GOAL: return (r, c)
        return None

    def find_agent(self, grid):
        for r, row in enumerate(grid):
            for c, val in enumerate(row):
                if val == AGENT: return (r, c)
        return None

def create_pressure_plate_problem(game):
    return PressurePlateProblem(game)