import pygame
import time
from ex1 import create_pressure_plate_problem  # נניח שהקובץ שלך נקרא ex1.py

# צבעים
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
BLUE = (100, 100, 255)
RED = (255, 100, 100)
GREEN = (100, 255, 100)
YELLOW = (255, 255, 100)

# קבועים
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


def draw_board(screen, grid, font):
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            val = grid[row][col]

            rect = pygame.Rect(col * CELL_SIZE, row *
                               CELL_SIZE, CELL_SIZE, CELL_SIZE)

            if val == WALL:
                color = BLACK
            elif val == FLOOR:
                color = WHITE
            elif val == AGENT or val == AGENT_ON_GOAL:
                color = BLUE
            elif val == GOAL:
                color = GREEN
            elif val in KEY_BLOCKS:
                color = RED
            elif val in PRESSURE_PLATES:
                color = YELLOW
            elif val in PRESSED_PLATES:
                color = (255, 165, 0)
            elif val in LOCKED_DOORS:
                color = GRAY
            else:
                color = WHITE

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)

            text = font.render(str(val), True, BLACK)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)


def run_simulation():
    initial_state = (
        (99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99),
        (99, 1, 10, 20, 99, 98, 98, 98, 99, 98, 16, 26, 99),
        (99, 11, 98, 98, 40, 98, 12, 22, 99, 98, 98, 98, 99),
        (99, 21, 98, 98, 99, 98, 98, 98, 99, 98, 98, 98, 99),
        (99, 99, 41, 99, 99, 99, 42, 99, 99, 99, 42, 99, 99),
        (99, 98, 98, 98, 99, 98, 98, 98, 99, 98, 98, 98, 99),
        (99, 98, 98, 98, 43, 15, 25, 98, 42, 98, 98, 98, 99),
        (99, 98, 98, 98, 99, 98, 14, 24, 99, 98, 98, 98, 99),
        (99, 99, 41, 99, 99, 99, 99, 99, 99, 99, 46, 99, 99),
        (99, 98, 98, 98, 99, 98, 98, 98, 99, 98, 98, 98, 99),
        (99, 13, 98, 98, 44, 98, 98, 98, 45, 98, 2, 98, 99),
        (99, 23, 98, 98, 99, 98, 98, 98, 99, 98, 98, 98, 99),
        (99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99),


    )

    # actions = ['U', 'L', 'U', 'R', 'U', 'L', 'L', 'D', 'L', 'D', 'L', 'L', 'L', 'L', 'D', 'L', 'U', 'U', 'U', 'R', 'U', 'L', 'D', 'L', 'D', 'D', 'D', 'L', 'L', 'L', 'U', 'U', 'U', 'U', 'U', 'R', 'R', 'R', 'U', 'U', 'L', 'L', 'L', 'U', 'U', 'U', 'U', 'U', 'R', 'R', 'D', 'D', 'D', 'R']
    actions = ['D', 'U', 'U', 'L', 'D', 'D', 'R', 'D', 'L', 'L', 'U', 'R', 'U', 'U', 'L', 'L']
    pygame.init()
    screen = pygame.display.set_mode(
        (len(initial_state[0]) * CELL_SIZE, len(initial_state) * CELL_SIZE))
    pygame.display.set_caption("Pressure Plate Simulation")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    problem = create_pressure_plate_problem(initial_state)
    state = (initial_state, problem.find_agent(initial_state), 0)

    for action in actions:
        for a, next_state in problem.successor(state):
            if a == action:
                state = next_state
                break

        draw_board(screen, state[0], font)
        pygame.display.flip()
        time.sleep(100)
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

    pygame.quit()


if __name__ == "__main__":
    run_simulation()
