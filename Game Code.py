import pygame
from pygame.locals import *
import random

# Initialises pygame
pygame.init()

# Screen background images
main_menu = pygame.image.load('main_menu.png')
instructions_screen = pygame.image.load('instructions_screen.png')
settings_screen = pygame.image.load('settings_screen.png')
game_screen = pygame.image.load('game_screen.png')
completion_screen = pygame.image.load('completion_screen.png')

# Button images
play_button = pygame.image.load('play_button.png')
settings_button = pygame.image.load('settings_button.png')
instructions_button = pygame.image.load('instructions_button.png')
home_button = pygame.image.load('home_button.png')
back_button = pygame.image.load('back_button.png')

# Other components of the interface
character = pygame.image.load('character.png')
skeleton = pygame.image.load('skeleton.png')
grass = pygame.image.load('grass.jpg')
controls = pygame.image.load('touch_controls.png')
bone = pygame.image.load('bone.png')
shine = pygame.image.load('shine.png')
up_arrow = pygame.image.load('up_arrow.png')
down_arrow = pygame.image.load('down_arrow.png')
left_arrow = pygame.image.load('left_arrow.png')
right_arrow = pygame.image.load('right_arrow.png')

# Setting up screen dimensions
Width, Height = 1180, 820
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Maze Game")

# Resizing button images
button_width, button_height = 236, 113
play_button = pygame.transform.scale(play_button, (button_width, button_height))
instructions_button = pygame.transform.scale(instructions_button, (button_width, button_height))
settings_button = pygame.transform.scale(settings_button, (button_width, button_height))
back_button = pygame.transform.scale(back_button, (button_width - 20, button_height))
home_button = pygame.transform.scale(home_button, (button_width - 60, button_height - 40))
shine = pygame.transform.scale(shine, (1534, 780))
up_arrow = pygame.transform.scale(up_arrow, (58, 82))
down_arrow = pygame.transform.scale(down_arrow, (58, 82))
left_arrow = pygame.transform.scale(left_arrow, (82, 58))
right_arrow = pygame.transform.scale(right_arrow, (82, 58))


# Defining button dimensions and spacings
button_x = (Width - button_width) // 2
button_spacing = 20  # The space between the buttons

# Defining button positions
play_button_position = play_button.get_rect(topleft=(button_x, 300))
instructions_button_position = instructions_button.get_rect(topleft=(button_x, play_button_position.bottom + button_spacing))
settings_button_position = settings_button.get_rect(topleft=(button_x, instructions_button_position.bottom + button_spacing))
back_button_position = back_button.get_rect(bottomleft=(-35, Height - 20))
home_button_position = home_button.get_rect(topleft=(-35, Height - 85))
up_arrow_position = up_arrow.get_rect(bottomright=(1020, 500))
down_arrow_position = down_arrow.get_rect(bottomright=(1020, 590))
left_arrow_position = left_arrow.get_rect(bottomright=(957, 555))
right_arrow_position = right_arrow.get_rect(bottomright=(1060, 555))


white = (255, 255, 255)
black = (1,1,1)
red = (255,0,0)
gray = (100,100,100)

Rows, Cols = 10, 10
player_row, player_col = 1, 1
Bone_count = 0

game_state = "menu"

MazeGrid = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

def Random_position():
    while True:
        row = random.randint(1, Rows -2)
        col = random.randint(1, Cols -2)
        if MazeGrid[row][col] == 0 and (row, col) != (player_row, player_col):
            return row,col


collectible_row = 0
collectible_col = 0
collectible_row, collectible_col = Random_position()

def draw_menu():
    screen.blit(main_menu, (0, 0))  # Sets background
    screen.blit(play_button, play_button_position.topleft)
    screen.blit(instructions_button, instructions_button_position.topleft)
    screen.blit(settings_button, settings_button_position.topleft)

def draw_instructions():
    screen.blit(instructions_screen, (0, 0))
    screen.blit(back_button, back_button_position.topleft)

def draw_settings():
    screen.blit(settings_screen, (0, 0))
    screen.blit(back_button, back_button_position.topleft)

def draw_maze():
    # Initialising maze
    screen.blit(game_screen, (0, 0))
    maze_x_offset = 15  # Shift maze to the right slightly
    maze_y_offset = 250  # Shift maze down slightly
    Cell_Size = 60
    maze_width = Cols * Cell_Size
    maze_height = Rows * Cell_Size
    pygame.draw.rect(screen, (222,184,135), (305, maze_y_offset, maze_width, maze_height))

    # Initialising grass
    grass.convert_alpha()
    bush = pygame.transform.scale(grass, (Cell_Size, Cell_Size))

    # Initialising player
    x_offset = (Width - (Cell_Size*Cols))//2
    player_size = Cell_Size // 2
    player_offset = (Cell_Size - player_size) // 2  # centers the player in the cell

    # draw the maze
    for row in range(Rows):
        for col in range(Cols):
            x, y = maze_x_offset + x_offset + col * Cell_Size, maze_y_offset + row * Cell_Size
            if MazeGrid[row][col] == 1:
                screen.blit(bush, (x, y))

    # Draw collectible bone
    collectible_x = maze_x_offset + x_offset + collectible_col * Cell_Size + player_offset
    collectible_y = maze_y_offset + collectible_row * Cell_Size + player_offset
    pygame.draw.circle(screen, (0, 255, 0), (collectible_x + player_size // 2, collectible_y+ player_size // 2), player_size //3)

    # Draw player
    player_x = maze_x_offset + x_offset + player_col * Cell_Size + player_offset
    player_y = maze_y_offset + player_row * Cell_Size + player_offset
    pygame.draw.rect(screen, red, (player_x, player_y, player_size, player_size))

    # Draw bone counter
    Bone_text = (pygame.font.Font(None, 50)).render(f"{Bone_count}", True, black)
    screen.blit(Bone_text, (250, 250))

    # Back button
    screen.blit(back_button, back_button_position.topleft)

    # Draw touch controls
    screen.blit(up_arrow, up_arrow_position.bottomright)
    screen.blit(down_arrow, down_arrow_position.bottomright)
    screen.blit(left_arrow, left_arrow_position.bottomright)
    screen.blit(right_arrow, right_arrow_position.bottomright)

shine_scale = 1.3  # Initial scale (1.0 = original size)
scale_direction = 0.0065  # Speed of scaling (adjust for faster/slower effect)

def draw_completion_screen():
    screen.blit(completion_screen, (0, 0))
    screen.blit(home_button, home_button_position.topleft)

    global shine_scale, scale_direction
    shine_scale += scale_direction  # Increase or decrease scale

    # Reverse direction when hitting size limits
    if shine_scale >= 1.56 or shine_scale <= 1.04:
        scale_direction *= -1

    # Scale the shine image
    new_size = (int(800 * shine_scale), int(400 * shine_scale))
    shine_resized = pygame.transform.scale(shine, new_size)

    # Calculate position to keep it centered
    shine_x = 190 - (new_size[0] - 800) // 2
    shine_y = 80 - (new_size[1] - 800) // 2

    # Draw the pulsating shine
    screen.blit(shine_resized, (shine_x, shine_y))

    # Draw the skeleton on top
    screen.blit(skeleton, (200, 270))

slider_x = 200
slider_y = 500
slider_width = 400
slider_height = 10
knob_radius = 10
knob_x = slider_x + slider_width // 2  # Start in the middle
brightness = 1.0  # 1.0 = normal, <1.0 = darker

def Move_player(dx, dy):
    global player_row, player_col, collectible_col, collectible_row, Bone_count
    new_row = player_row + dy
    new_col = player_col + dx

    #check movement is allowed, not into a wall
    if 0 <= new_row < Rows and 0 <= new_col < Cols and MazeGrid[new_row][new_col] == 0:
        player_row, player_col = new_row, new_col

        if player_row == collectible_row and player_col == collectible_col:
            Bone_count +=1
            collectible_row, collectible_col = Random_position() # spawn a new item

running = True
while running:
    # screen.fill(pathcolour)
    screen.fill((255, 255, 255)) # White background

    if game_state == 'menu':
        draw_menu()
    elif game_state == 'game':
        draw_maze()
        pass
    elif game_state == 'instructions':
        draw_instructions()
        pass
    elif game_state == 'settings':
        draw_settings()
        pass
    elif game_state == 'complete':
        draw_completion_screen()
    if Bone_count == 10:
        game_state = 'complete'
        Bone_count = 0

    # controls the event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if game_state == 'menu':
                if play_button_position.collidepoint(mouse_pos):
                    overlay = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
                    overlay.fill((0, 153, 0, 51))  # Green overlay
                    screen.blit(play_button, play_button_position.topleft)
                    screen.blit(overlay, play_button_position.topleft)
                    pygame.display.flip()
                    pygame.time.delay(150)
                    game_state = 'game'
                elif instructions_button_position.collidepoint(mouse_pos):
                    overlay = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
                    overlay.fill((0, 153, 0, 51))  # Green overlay
                    screen.blit(instructions_button, instructions_button_position.topleft)
                    screen.blit(overlay, instructions_button_position.topleft)
                    pygame.display.flip()
                    pygame.time.delay(150)
                    game_state = 'instructions'
                elif settings_button_position.collidepoint(mouse_pos):
                    overlay = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
                    overlay.fill((0, 153, 0, 51))  # Green overlay
                    screen.blit(settings_button, settings_button_position.topleft)
                    screen.blit(overlay, settings_button_position.topleft)
                    pygame.display.flip()
                    pygame.time.delay(150)
                    game_state = 'settings'
            elif game_state in ['instructions', 'settings', 'game']:
                if back_button_position.collidepoint(mouse_pos):
                    game_state = 'menu'
            elif game_state == 'complete':
                if home_button_position.collidepoint(mouse_pos):
                    game_state = 'menu'

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and game_state in ['instructions', 'settings', 'game']:
                game_state = 'menu'
            elif event.key == K_LALT:
                game_state = "settings"
            elif event.key == K_RETURN and game_state == "complete":
                game_state = "menu"
            elif game_state == "game":
                if event.key == K_LEFT or event.key == K_a:
                    Move_player(-1, 0)
                elif event.key == K_RIGHT or event.key == K_d:
                    Move_player(1, 0)
                elif event.key == K_UP or event.key == K_w:
                    Move_player(0, -1)
                elif event.key == K_DOWN or event.key == K_s:
                    Move_player(0, 1)
                elif event.key == K_p:
                    Bone_count = 10
                elif event.key == K_t:
                    game_state == "complete"
    pygame.display.flip()  # updates the display

pygame.quit()