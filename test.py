import pygame
import random
import sys

# Initialize Pygame
pygame.init()


# Load Background Image for Home Screen
home_bg_image_path = '1.jpg'  # Ensure this path is correct
home_bg_image = pygame.image.load(home_bg_image_path)


# Maze settings
maze_size = (10, 10)
cell_size = 40
maze_width, maze_height = maze_size
screen_width, screen_height = maze_width * cell_size, maze_height * cell_size

# Colors
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
black = (0, 0, 0)

# Setup display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Maze Runner Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Font for displaying text
font = pygame.font.Font(None, 36)

# Game settings
start_pos = (0, 0)
end_pos = (maze_width - 1, maze_height - 1)
score = 0
time_limit = 60  # seconds

def init_grid(maze_width, maze_height):
    grid = []
    for y in range(maze_height):
        row = []
        for x in range(maze_width):
            cell = {'visited': False, 'walls': [True, True, True, True]}  # top, right, bottom, left
            row.append(cell)
        grid.append(row)
    return grid

def draw_maze(grid):
    for y in range(maze_height):
        for x in range(maze_width):
            cell = grid[y][x]
            x0, y0 = x * cell_size, y * cell_size
            walls = cell['walls']
            # Draw walls
            if walls[0]: # Top
                pygame.draw.line(screen, white, (x0, y0), (x0 + cell_size, y0), 2)
            if walls[1]: # Right
                pygame.draw.line(screen, white, (x0 + cell_size, y0), (x0 + cell_size, y0 + cell_size), 2)
            if walls[2]: # Bottom
                pygame.draw.line(screen, white, (x0, y0 + cell_size), (x0 + cell_size, y0 + cell_size), 2)
            if walls[3]: # Left
                pygame.draw.line(screen, white, (x0, y0), (x0, y0 + cell_size), 2)

def carve_passages_from(cx, cy, grid):
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    random.shuffle(directions)
    grid[cy][cx]['visited'] = True

    for dx, dy in directions:
        nx, ny = cx + dx, cy + dy
        if (0 <= nx < maze_width) and (0 <= ny < maze_height) and not grid[ny][nx]['visited']:
            # Remove the wall between the current cell and the next cell
            if dx == 1:  # Moving right
                grid[cy][cx]['walls'][1] = False
                grid[ny][nx]['walls'][3] = False
            elif dx == -1: # Moving left
                grid[cy][cx]['walls'][3] = False
                grid[ny][nx]['walls'][1] = False
            elif dy == 1:  # Moving down
                grid[cy][cx]['walls'][2] = False
                grid[ny][nx]['walls'][0] = False
            elif dy == -1: # Moving up
                grid[cy][cx]['walls'][0] = False
                grid[ny][nx]['walls'][2] = False
            carve_passages_from(nx, ny, grid)

def generate_maze():
    grid = init_grid(maze_width, maze_height)
    start_x, start_y = start_pos
    carve_passages_from(start_x, start_y, grid)
    return grid

def display_score(score, time_left):
    score_text = font.render(f"Score: {score}", True, white)
    time_text = font.render(f"Time: {int(time_left)}", True, white)
    screen.blit(score_text, (10, 10))
    screen.blit(time_text, (screen_width - 150, 10))

def reset_game():
    global score
    maze = generate_maze()
    start_time = pygame.time.get_ticks()  # Reset the timer
    return maze, list(start_pos)

def show_popup_message(message, total_score):
    popup = font.render(f"{message} Total Score: {total_score}", True, white)
    popup_rect = popup.get_rect(center=(screen_width / 2, screen_height / 2))
    screen.fill(black)  # Optional: Fill the screen with black before displaying the message
    screen.blit(popup, popup_rect)
    pygame.display.flip()
    pygame.time.wait(2000)  # Display the message for 2 seconds



def show_home_screen():
    start_button = pygame.Rect(screen_width / 2 - 100, screen_height / 2, 200, 50)  # Adjust as necessary
    button_color = (0, 200, 0)
    text_color = (255, 255, 255)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if start_button.collidepoint(mouse_pos):
                    return  # Proceed to the main game

        screen.blit(home_bg_image, (0, 0))
        
        # Draw the title "Maze Game"
        title_font = pygame.font.Font(None, 64)  # Adjust font size and style as necessary
        title_text = title_font.render("Maze Game", True, text_color)
        title_text_rect = title_text.get_rect(center=(screen_width / 2, screen_height / 3))
        screen.blit(title_text, title_text_rect)


        # Draw the start button
        pygame.draw.rect(screen, button_color, start_button)
        start_text = font.render('Start', True, text_color)
        start_text_rect = start_text.get_rect(center=start_button.center)
        screen.blit(start_text, start_text_rect)
        
        # Draw "Made by Sarthak and Varun"
        credit_text = font.render("Made by Sarthak and Varun", True, red)
        credit_text_rect = credit_text.get_rect(center=(screen_width / 2, screen_height - 30))  # Adjust position as needed
        screen.blit(credit_text, credit_text_rect)

        pygame.display.flip()
        clock.tick(30)

# Main function to run the game
def main():
    show_home_screen()  # Display the home screen before starting the game
    global score
    player_pos = list(start_pos)
    maze = generate_maze()
    start_time = pygame.time.get_ticks()

    running = True
    while running:
        current_time = pygame.time.get_ticks()
        time_left = time_limit - (current_time - start_time) / 1000

        if time_left <= 0:
            show_popup_message("Time is over!", score)  # Display the popup message with total score
            score = 0  # Reset total score
            maze, player_pos = reset_game()  # Reset the game if time runs out
            start_time = pygame.time.get_ticks()  # Restart the timer after resetting


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Player movement
            if event.type == pygame.KEYDOWN:
                x, y = player_pos
                if event.key == pygame.K_LEFT and not maze[y][x]['walls'][3]:  # Left
                    player_pos[0] = max(0, x - 1) # type: ignore
                elif event.key == pygame.K_RIGHT and not maze[y][x]['walls'][1]:  # Right
                    player_pos[0] = min(maze_width - 1, x + 1) # type: ignore
                elif event.key == pygame.K_UP and not maze[y][x]['walls'][0]:  # Up
                    player_pos[1] = max(0, y - 1) # type: ignore
                elif event.key == pygame.K_DOWN and not maze[y][x]['walls'][2]:  # Down
                    player_pos[1] = min(maze_height - 1, y + 1) # type: ignore


                # Check for completion
                if player_pos == list(end_pos):
                    score += 1
                    maze, player_pos = reset_game()

        # Drawing the maze and other game elements
        screen.fill(black)
        draw_maze(maze)

        # Draw player
        px, py = player_pos
        pygame.draw.circle(screen, green, (px * cell_size + cell_size // 2, py * cell_size + cell_size // 2), cell_size // 3)

        # Draw end position
        ex, ey = end_pos
        pygame.draw.circle(screen, red, (ex * cell_size + cell_size // 2, ey * cell_size + cell_size // 2), cell_size // 3)

        display_score(score, time_left)
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()