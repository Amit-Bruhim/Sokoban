import pygame
import time
from ex1 import create_pressure_plate_problem

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BLUE = (100, 100, 255)    # Agent
RED = (255, 100, 100)     # Key Blocks
GREEN = (100, 255, 100)   # Goal
YELLOW = (255, 255, 100)  # Pressure Plates
ORANGE = (255, 165, 0)    # Pressed Plates
MAGENTA = (255, 0, 255)   # Agent on Goal (New Color!)

# Constants
CELL_SIZE = 60
WALL = 99
FLOOR = 98
AGENT = 1
GOAL = 2
AGENT_ON_GOAL = 3
KEY_BLOCKS = list(range(10, 20))
PRESSURE_PLATES = list(range(20, 30))
PRESSED_PLATES = list(range(30, 40))
LOCKED_DOORS = list(range(40, 50))

def build_grid(state, rows, cols, initial_map):
    """
    Reconstructs the grid from the logical state for visualization.
    """
    agent_pos, keys, plates, doors, _ = state
    
    # Start with a grid containing only static elements (Walls and Goals)
    grid = [[initial_map[r][c] if initial_map[r][c] in [WALL, GOAL] else FLOOR 
             for c in range(cols)] for r in range(rows)]
    
    # 1. Place Pressure Plates (Check if they are active or pressed)
    for r in range(rows):
        for c in range(cols):
            val = initial_map[r][c]
            if val in PRESSURE_PLATES:
                is_active = any(p[0] == r and p[1] == c for p in plates)
                if is_active:
                    grid[r][c] = val
                else:
                    grid[r][c] = val + 10

    # 2. Place Locked Doors from state
    for r, c, val in doors:
        grid[r][c] = val
        
    # 3. Place Key Blocks from state
    for r, c, val in keys:
        grid[r][c] = val

    # 4. Place the Agent and handle Agent-on-Goal (Value 3)
    ar, ac = agent_pos
    if initial_map[ar][ac] == GOAL:
        grid[ar][ac] = AGENT_ON_GOAL
    else:
        grid[ar][ac] = AGENT
    
    return grid

def draw_board(screen, grid, font):
    """ Renders the reconstructed grid to the screen """
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            val = grid[row][col]
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)

            # Determine color based on cell value
            if val == WALL:
                color = BLACK
            elif val == FLOOR:
                color = WHITE
            elif val == AGENT:
                color = BLUE
            elif val == AGENT_ON_GOAL:
                color = MAGENTA # New distinctive color for Agent on Goal
            elif val == GOAL:
                color = GREEN
            elif val in KEY_BLOCKS:
                color = RED
            elif val in PRESSURE_PLATES:
                color = YELLOW
            elif val in PRESSED_PLATES:
                color = ORANGE
            elif val in LOCKED_DOORS:
                color = GRAY
            else:
                color = WHITE

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRAY, rect, 1) # Cell border

            # Render the ID number of the object
            text = font.render(str(val), True, BLACK)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

def run_simulation():
    # The map structure with the 99 border
    initial_map = (
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

    # Sequence of moves
    actions = ['R', 'R', 'D', 'R', 'R', 'U', 'R', 'L', 'D', 'L', 'L', 'D', 'D', 'D', 'L', 'L', 'D', 'U', 'R', 'R', 'U', 'U', 'U', 'R', 'R', 'D', 'R', 'R', 'R', 'D', 'D', 'L', 'L', 'L', 'D', 'D', 'L', 'R', 'R', 'R', 'D', 'R']
    
    pygame.init()
    rows, cols = len(initial_map), len(initial_map[0])
    screen = pygame.display.set_mode((cols * CELL_SIZE, rows * CELL_SIZE))
    pygame.display.set_caption("Sokoban Pressure Plate Sim")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    # Initialize the problem and state
    problem = create_pressure_plate_problem(initial_map)
    state = (
        problem.find_agent(initial_map),
        problem.find_key_blocks(initial_map),
        problem.find_pressure_plates(initial_map),
        problem.find_locked_doors(initial_map),
        0
    )

    # DRAW INITIAL STATE BEFORE WAITING
    current_grid = build_grid(state, rows, cols, initial_map)
    screen.fill(WHITE)
    draw_board(screen, current_grid, font)
    pygame.display.flip()

    # WAIT FOR 2 SECONDS BEFORE STARTING
    time.sleep(2)

    # Main simulation loop
    for action in actions:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        for a, next_state in problem.successor(state):
            if a == action:
                state = next_state
                break
        
        current_grid = build_grid(state, rows, cols, initial_map)
        screen.fill(WHITE)
        draw_board(screen, current_grid, font)
        pygame.display.flip()
        
        time.sleep(0.5) 
        clock.tick(60)

    time.sleep(1.5)
    pygame.quit()

if __name__ == "__main__":
    run_simulation()