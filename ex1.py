# I used AI tools including ChatGPT, Gemini, and GitHub Copilot during the development of this code.
# I also discussed ideas and received input from peers in the course WhatsApp group.


import ex1_check
import search
import utils

id = ["211548045"]

""" Rules """
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
directions = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1)
}

""" This class implements a pressure plate problem """


class PressurePlateProblem(search.Problem):
    """This class implements a pressure plate problem"""

    def __init__(self, initial):
        self.visited_states = set()
        self.map = initial
        goal = self.find_goal(initial)
        self.goal = goal
        agent = self.find_agent(initial)
        g = 0
        key_blocks = self.find_key_blocks(initial)
        pressure_plates = self.find_pressure_plates(initial)
        locked_doors = self.find_locked_doors(initial)
        state = (agent, key_blocks, pressure_plates, locked_doors, g)
        """ Constructor only needs the initial state.
        Don't forget to set the goal or implement the goal test"""
        search.Problem.__init__(self, state, goal)

    def successor(self, state):
        """ Generates the successor states returns [(action, achieved_states, ...)]"""
        
        # print("successor")
        successors = []
        for direction, delta in directions.items():
            is_valid, new_state = self.make_move(state, direction)
            if is_valid:
                state_key = self.canonical_state(new_state)
                if state_key not in self.visited_states:
                    self.visited_states.add(state_key)
                    successors.append((direction, new_state))
        return successors

    def goal_test(self, state):
        """ given a state, checks if this is the goal state, compares to the created goal state returns True/False"""
        # print("goal_test")
        agent = state[0]
        goal = self.goal
        
        if agent[0] == goal[0] and agent[1] == goal[1]:
            return True
        return False
            
    def h(self, node):
        """ This is the heuristic. It gets a node (not a state)
        and returns a goal distance estimate"""
        # open the node and get the state
        agent, key_blocks, pressure_plates, locked_doors, g = node.state  
        goal = self.goal
        
        # define factor of lamda
        # lamda = 1
        
        # punish locked doors
        locked_doors_amount = len(locked_doors)
        
        # punish diatance to pressure plates
        key_plate_distances = 0
        for key in key_blocks:
            key_x, key_y, key_type = key
            min_dist = float('inf')
            for plate in pressure_plates:
                plate_x, plate_y, plate_type = plate
                if self.same_type(key_type, plate_type):
                    dist = abs(plate_x - key_x) + abs(plate_y - key_y)
                    if dist < min_dist:
                        min_dist = dist

            if min_dist == float('inf'):
                key_plate_distances += 30
            else:
                key_plate_distances += min_dist

        # punish keys in corners
        corner_keys = 0
        for key_block in key_blocks:
            walls = 0
            for direction, delta in directions.items():
                new_pos = (key_block[0] + delta[0], key_block[1] + delta[1])
                if self.map[new_pos[0]][new_pos[1]] == WALL:
                    walls += 1
                if walls >= 2:
                    corner_keys += 1
                    break
            if corner_keys:
                break
        
        # Manhattan distance 
        manhattan_distance = abs(agent[0] - goal[0]) + abs(agent[1] - goal[1])
        
        # define h
        h = 2 * manhattan_distance + 1.8 * key_plate_distances + corner_keys * 5 + locked_doors_amount  + 1.5 * g
        
        # return h
        return 10 * h

    def canonical_state(self, state):
        agent, key_blocks, pressed_plates, locked_doors, g = state
        key_blocks = tuple(sorted(key_blocks))
        pressed_plates = tuple(sorted(pressed_plates))
        locked_doors = tuple(sorted(locked_doors))
        return (agent, key_blocks, pressed_plates, locked_doors)

    def find_key_blocks(self, map): 
        """ given a map, return all key blocks positions"""
        key_blocks = []
        for i, row in enumerate(map):
            for j, cell in enumerate(row):
                if cell in KEY_BLOCKS:
                    key_blocks.append((i, j, cell))
        return frozenset(key_blocks)

    def find_locked_doors(self, map):
        """Given a map, return all locked doors positions."""
        locked_doors = []
        for i, row in enumerate(map):
            for j, cell in enumerate(row):
                if cell in LOCKED_DOORS:
                    locked_doors.append((i, j, cell))
        return frozenset(locked_doors)

    def find_pressure_plates(self, map):
        """ given a map, return all pressure plates positions"""
        pressure_plates = []
        for i, row in enumerate(map):
            for j, cell in enumerate(row):
                if cell in PRESSURE_PLATES:
                    pressure_plates.append((i, j, cell))
        return frozenset(pressure_plates)

    def make_move(self, state, action):
        """ given a state and an action, returns the new state"""
        is_valid = False
        old_agent, key_blocks, pressure_plates, locked_doors, g = state   
        dx, dy = directions[action]
        new_agent_pos = (old_agent[0] + dx, old_agent[1] + dy)
        new_cell_val = ()
        for pos in key_blocks:
            if pos[0] == new_agent_pos[0] and pos[1] == new_agent_pos[1]:
                
                second_cell_pos = (pos[0] + dx, pos[1] + dy)
                for position in key_blocks:
                    if position[0] == second_cell_pos[0] and position[1] == second_cell_pos[1]:
                        return False, state
                for position in locked_doors:
                    if position[0] == second_cell_pos[0] and position[1] == second_cell_pos[1]:
                        return False, state
                for position in pressure_plates:
                    if position[0] == second_cell_pos[0] and position[1] == second_cell_pos[1]:
                        if not self.same_type(pos[2], position[2]):
                            return False, state
                        else:
                            new_cell_val = position[2] + 10
                            new_position = (second_cell_pos[0], second_cell_pos[1], new_cell_val)
                            updated_pressure_plates = frozenset(pressure_plates - {position})
                            updated_key_blocks = frozenset(key_blocks - {pos})
                            updated_locked_doors = locked_doors
                            is_remaining_locks = False
                            for plate in updated_pressure_plates:
                                if self.same_type(plate[2], new_cell_val):
                                    is_remaining_locks = True
                                    break
                            if not is_remaining_locks:
                                for door in locked_doors:
                                    if door[2] == position[2] + 20:
                                        updated_locked_doors = frozenset(updated_locked_doors - {door})
                                    
                            return True, (new_agent_pos, updated_key_blocks, updated_pressure_plates, updated_locked_doors, g + 1)
                new_cell_val = self.map[second_cell_pos[0]][second_cell_pos[1]]
                if new_cell_val == WALL or new_cell_val == GOAL or new_cell_val in PRESSURE_PLATES:
                    return False, state
                else:
                    updated_key_blocks = frozenset((key_blocks - {pos}) | {(second_cell_pos[0], second_cell_pos[1], pos[2])})
                    return True, (new_agent_pos, updated_key_blocks, pressure_plates, locked_doors, g + 1)
        for pos in locked_doors:
            if pos[0] == new_agent_pos[0] and pos[1] == new_agent_pos[1]:
                return False, state
        for pos in pressure_plates: 
            if pos[0] == new_agent_pos[0] and pos[1] == new_agent_pos[1]:
                return False, state
        new_cell_val = self.map[new_agent_pos[0]][new_agent_pos[1]]
        if new_cell_val == WALL or new_cell_val in PRESSURE_PLATES:
            return False, state
        else:
            return True, (new_agent_pos, key_blocks, pressure_plates, locked_doors, g + 1)
            
        # if new_cell_val in LOCKED_DOORS or new_cell_val == WALL or new_cell_val in PRESSURE_PLATES or new_cell_val in PRESSED_PLATES:
        #     return is_valid, state
        # if new_cell_val == FLOOR:
        #     new_map[old_agent[0]][old_agent[1]] = FLOOR
        #     new_map[new_agent_pos[0]][new_agent_pos[1]] = AGENT
        #     is_valid = True
        # elif new_cell_val == GOAL:
        #     new_map[old_agent[0]][old_agent[1]] = FLOOR
        #     new_map[new_agent_pos[0]][new_agent_pos[1]] = AGENT_ON_GOAL
        #     is_valid = True
        # elif new_cell_val in KEY_BLOCKS:
        #     second_cell_pos = (new_agent_pos[0] + dx, new_agent_pos[1] + dy)
        #     second_cell_val = new_map[second_cell_pos[0]][second_cell_pos[1]]
        #     if second_cell_val == FLOOR:
        #         new_map[old_agent[0]][old_agent[1]] = FLOOR
        #         new_map[new_agent_pos[0]][new_agent_pos[1]] = AGENT
        #         new_map[second_cell_pos[0]][second_cell_pos[1]] = new_cell_val
        #         is_valid = True
        #     elif second_cell_val in PRESSURE_PLATES and self.same_type(new_cell_val, second_cell_val):
        #         new_map[old_agent[0]][old_agent[1]] = FLOOR
        #         new_map[new_agent_pos[0]][new_agent_pos[1]] = AGENT
        #         new_map[second_cell_pos[0]][second_cell_pos[1]] = second_cell_val + 10
        #         # open door if needed
        #         is_locked_door_exist = False
        #         for i in range(len(new_map)):
        #             for j in range(len(new_map[i])):
        #                 if new_map[i][j] in LOCKED_DOORS and self.same_type(new_map[i][j], second_cell_val):
        #                     is_locked_door_exist = True
        #                     break
        #         if is_locked_door_exist:
        #             for i in range(len(new_map)):
        #                 for j in range(len(new_map[i])):
        #                     if new_map[i][j] == second_cell_val + 20:
        #                         new_map[i][j] = FLOOR
        #         is_valid = True
        # new_map = tuple(tuple(row) for row in new_map)
        # return is_valid, (new_map, new_agent_pos, g + 1)
            
    def same_type(self, cell1_val, cell2_val):
        """ given two cell values, checks if they are the same type"""
        return cell1_val % 10 == cell2_val % 10

    def find_goal(self, map):
        """ given a map, return it's goal position"""
        for i, row in enumerate(map):
            for j, cell in enumerate(row):
                if cell == GOAL:
                    return (i, j)
        return None

    def find_agent(self, map):
        """ given a map, return the agent position"""
        for i, row in enumerate(map):
            for j, cell in enumerate(row):
                if cell == AGENT:
                    return (i, j)
        return None

def create_pressure_plate_problem(game):
    print("<<create_pressure_plate_problem")
    """ Create a pressure plate problem, based on the description.
    game - tuple of tuples as described in pdf file"""
    return PressurePlateProblem(game)


if __name__ == '__main__':
    ex1_check.main()
