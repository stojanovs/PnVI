import pygame
import sys

# Initialize Pygame
pygame.init()

WINDOW_DIMENSIONS = 500
GRID_DIMENSIONS = 5
CELL_DIMENSION = WINDOW_DIMENSIONS // GRID_DIMENSIONS
COLOR_PALETTE = {
    "WHITE": (255, 255, 255),
    "RED": (255, 0, 0),
    "PINK": (255, 192, 203),
    "DARK_GRAY": (169, 169, 169),
    "YELLOW": (255, 255, 0),
}
screen = pygame.display.set_mode((WINDOW_DIMENSIONS, WINDOW_DIMENSIONS + 50))
pygame.display.set_caption("Color Fill Game")

game_grid = [["WHITE" for _ in range(GRID_DIMENSIONS)] for _ in range(GRID_DIMENSIONS)]
selected_color = "WHITE"


def render_grid():
    for row in range(GRID_DIMENSIONS):
        for col in range(GRID_DIMENSIONS):
            cell_color = COLOR_PALETTE[game_grid[row][col]]
            pygame.draw.rect(
                screen,
                cell_color,
                (col * CELL_DIMENSION, row * CELL_DIMENSION, CELL_DIMENSION, CELL_DIMENSION),
            )
            pygame.draw.rect(
                screen,
                (0, 0, 0),
                (col * CELL_DIMENSION, row * CELL_DIMENSION, CELL_DIMENSION, CELL_DIMENSION),
                1,
            )


def render_color_palette():
    """Render the color selection palette."""
    palette_y = WINDOW_DIMENSIONS  # Below the grid
    button_width = WINDOW_DIMENSIONS // len(COLOR_PALETTE)
    for index, (color_name, color_value) in enumerate(COLOR_PALETTE.items()):
        pygame.draw.rect(
            screen,
            color_value,
            (index * button_width, palette_y, button_width, 100)
        )
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (index * button_width, palette_y, button_width, 100),
            1
        )


def draw_popup_message(message):
    popup_width, popup_height = 300, 100
    popup_x = (WINDOW_DIMENSIONS - popup_width) // 2
    popup_y = (WINDOW_DIMENSIONS - popup_height) // 2
    pygame.draw.rect(screen, (200, 200, 200), (popup_x, popup_y, popup_width, popup_height))
    pygame.draw.rect(screen, (0, 0, 0), (popup_x, popup_y, popup_width, popup_height), 2)
    font = pygame.font.Font(None, 30)
    text = font.render(message, True, (0, 0, 0))
    text_rect = text.get_rect(center=(popup_x + popup_width // 2, popup_y + popup_height // 2))
    screen.blit(text, text_rect)


def get_color_from_palette(mouse_x, mouse_y):
    palette_y = WINDOW_DIMENSIONS
    if palette_y <= mouse_y <= palette_y + 50:
        button_width = WINDOW_DIMENSIONS // len(COLOR_PALETTE)
        color_index = mouse_x // button_width
        return list(COLOR_PALETTE.keys())[color_index]

def is_color_change_allowed(row, col, new_color):

    neighbors = [
        (row - 1, col),
        (row + 1, col),
        (row, col - 1),
        (row, col + 1),
    ]
    for neighbor_row, neighbor_col in neighbors:
        if 0 <= neighbor_row < GRID_DIMENSIONS and 0 <= neighbor_col < GRID_DIMENSIONS:
            if game_grid[neighbor_row][neighbor_col] == new_color:
                return False
    return True

def is_game_finished():
    for row in game_grid:
        if "WHITE" in row:
            return False
    return True


def main():
    global selected_color
    is_running = True
    show_popup = False
    popup_timer = 0
    popup_message = ""

    while is_running:
        screen.fill(COLOR_PALETTE["WHITE"])
        render_grid()
        render_color_palette()

        if show_popup:
            draw_popup_message(popup_message)
            popup_timer -= 1
            if popup_timer <= 0:
                show_popup = False

        if is_game_finished():
            draw_popup_message("Играта заврши! Ти Успеа!")
            pygame.display.flip()
            pygame.time.delay(3000)
            is_running = False
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                # Check if a color is selected from the palette
                if mouse_y >= WINDOW_DIMENSIONS:
                    color = get_color_from_palette(mouse_x, mouse_y)
                    if color:
                        selected_color = color
                else:
                    # Handle cell coloring
                    selected_col, selected_row = mouse_x // CELL_DIMENSION, mouse_y // CELL_DIMENSION
                    if is_color_change_allowed(selected_row, selected_col, selected_color):
                        game_grid[selected_row][selected_col] = selected_color
                    else:
                        popup_message = "Избраната боја не е дозволена за таа ќелија!"
                        show_popup = True
                        popup_timer = 240

        pygame.display.flip()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
