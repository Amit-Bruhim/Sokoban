import os
import warnings

# Suppress warnings and pygame welcome message before imports
warnings.filterwarnings("ignore", category=UserWarning)
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import time
from search_problem import create_pressure_plate_problem

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BLUE = (100, 100, 255)    # Agent
RED = (255, 100, 100)     # Key Blocks
GREEN = (100, 255, 100)   # Goal
YELLOW = (255, 255, 100)  # Pressure Plates
ORANGE = (255, 165, 0)    # Pressed Plates
MAGENTA = (255, 0, 255)   # Agent on Goal

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
    Reconstructs the visual grid based on the current logical state.
    Handles static elements (walls, goals) and dynamic elements (agent, blocks, plates).
    """
    agent_pos, keys, plates, doors, _ = state
    
    # Initialize grid with static elements (Walls and Goals)
    grid = [[initial_map[r][c] if initial_map[r][c] in [WALL, GOAL] else FLOOR 
             for c in range(cols)] for r in range(rows)]
    
    # 1. Update Pressure Plates (Show as pressed if no longer in 'plates' list)
    for r in range(rows):
        for c in range(cols):
            val = initial_map[r][c]
            if val in PRESSURE_PLATES:
                is_active = any(p[0] == r and p[1] == c for p in plates)
                if is_active:
                    grid[r][c] = val
                else:
                    grid[r][c] = val + 10 # Convert to Pressed Plate ID

    # 2. Place Locked Doors
    for r, c, val in doors:
        grid[r][c] = val
        
    # 3. Place Key Blocks
    for r, c, val in keys:
        grid[r][c] = val

    # 4. Place the Agent
    ar, ac = agent_pos
    if initial_map[ar][ac] == GOAL:
        grid[ar][ac] = AGENT_ON_GOAL
    else:
        grid[ar][ac] = AGENT
    
    return grid

def draw_board(screen, grid, font):
    """ Renders the grid and object IDs to the Pygame window """
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            val = grid[row][col]
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)

            if val == WALL:
                color = BLACK
            elif val == FLOOR:
                color = WHITE
            elif val == AGENT:
                color = BLUE
            elif val == AGENT_ON_GOAL:
                color = MAGENTA
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

            # Render ID text in the center of the cell
            text = font.render(str(val), True, BLACK)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

def run_simulation(initial_map, actions):
    """
    Main simulation loop. Receives the map and solution actions,
    then executes them step-by-step using the problem logic.
    """
    pygame.init()
    rows, cols = len(initial_map), len(initial_map[0])
    screen = pygame.display.set_mode((cols * CELL_SIZE, rows * CELL_SIZE))
    pygame.display.set_caption("Sokoban Pressure Plate Sim")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    # Initialize logic from search_problem
    problem = create_pressure_plate_problem(initial_map)
    state = (
        problem.find_agent(initial_map),
        problem.find_key_blocks(initial_map),
        problem.find_pressure_plates(initial_map),
        problem.find_locked_doors(initial_map),
        0
    )

    # Initial frame display
    current_grid = build_grid(state, rows, cols, initial_map)
    screen.fill(WHITE)
    draw_board(screen, current_grid, font)
    pygame.display.flip()
    time.sleep(1.5)

    # Execute actions
    for action in actions:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Find the next state based on the current action
        for a, next_state in problem.successor(state):
            if a == action:
                state = next_state
                break
        
        # Update display
        current_grid = build_grid(state, rows, cols, initial_map)
        screen.fill(WHITE)
        draw_board(screen, current_grid, font)
        pygame.display.flip()
        
        time.sleep(0.4) 
        clock.tick(60)

    time.sleep(1.5)
    pygame.quit()