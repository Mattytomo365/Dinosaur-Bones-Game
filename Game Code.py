import pygame
from pygame.locals import *
import random

# Initialises pygame
pygame.init()

# Setting up screen dimensions
Width, Height = 1180, 820
screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("Maze Game")

# Initialising sliders for settings screen
slider_x_volume = 250
slider_x_brightness = 250
slider_y_volume = 440
slider_y_brightness = 560
slider_width = 600
slider_height = 10
knob_radius = 20
knob_x_volume = slider_x_volume + slider_width // 2  # Initial positions of the knobs
knob_x_brightness = slider_x_brightness + slider_width // 2
volume = 0.5  # Default values
brightness = 1.0
is_dragging_volume = False
is_dragging_brightness = False

# Defining colours
white = (255, 255, 255)
black = (1,1,1)
red = (255,0,0)
gray = (100,100,100)

# Initialing maze components
Rows, Cols = 12, 12
player_row, player_col = 1, 1
Bone_count = 0
Cell_Size = Width//Cols

game_state = "menu"

# Screen background images
main_menu = pygame.image.load('main_menu.png')
instructions_screen = pygame.image.load('instructions_screen.png')
settings_screen = pygame.image.load('settings_screen.png')
game_screen = pygame.image.load('game_screen.png')
completion_screen = pygame.image.load('completion_screen.png')
information_screen = pygame.image.load('information_screen.png')

# Button images
play_button = pygame.image.load('play_button.png')
settings_button = pygame.image.load('settings_button.png')
instructions_button = pygame.image.load('instructions_button.png')
home_button = pygame.image.load('home_button.png')
back_button = pygame.image.load('back_button.png')
colour_blind_button = pygame.image.load('colour_blind_button.png')
information_button = pygame.image.load('information_button.png')

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
conversion_arrow = pygame.image.load('conversion_arrow.png')

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
colour_blind_button = pygame.transform.scale(colour_blind_button, (button_width * 0.75, button_height * 0.75))
information_button = pygame.transform.scale(information_button, (button_width * 0.75, button_height * 0.75))
conversion_arrow = pygame.transform.scale(conversion_arrow, (58, 82))
bone = pygame.transform.scale(bone, (Cell_Size // 2, Cell_Size // 2))
character = pygame.transform.scale(character, (Cell_Size // 2, Cell_Size // 1.4))



# Defining button dimensions and spacings
button_x = (Width - button_width) // 2
button_spacing = 20  # The space between the buttons

# Defining component/button positions
play_button_position = play_button.get_rect(topleft=(button_x, 300))
instructions_button_position = instructions_button.get_rect(topleft=(button_x, play_button_position.bottom + button_spacing))
settings_button_position = settings_button.get_rect(topleft=(button_x, instructions_button_position.bottom + button_spacing))
back_button_position = back_button.get_rect(bottomleft=(-35, Height - 20))
home_button_position = home_button.get_rect(topleft=(-35, Height - 85))
up_arrow_position = up_arrow.get_rect(topleft=(1010, 480))
down_arrow_position = up_arrow.get_rect(topleft=(1010, 580))
left_arrow_position = up_arrow.get_rect(topleft=(950, 540))
right_arrow_position = up_arrow.get_rect(topleft=(1050, 540))
colour_blind_button_position = colour_blind_button.get_rect(topleft=(50, 335))
information_button_position = information_button.get_rect(topleft=(940, 320))
conversion_arrow_position = conversion_arrow.get_rect(topleft=(830, 500))

def get_random_maze_position():
    while True:
        row = random.randint(1, Rows - 2)
        col = random.randint(1, Cols - 2)
        if maze[row][col] == 0:  # Ensure it's a valid path
            return row, col

Directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]

maze = [[1 for _ in range(Cols)] for _ in range (Rows)]



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

    # Draw Volume Slider
    pygame.draw.rect(screen, (85, 85, 43), (slider_x_volume, slider_y_volume, slider_width, slider_height))  # Slider bar
    pygame.draw.circle(screen, (184, 184, 148), (knob_x_volume, slider_y_volume + slider_height // 2), knob_radius)  # Knob

    # Draw Brightness Slider
    pygame.draw.rect(screen, (85, 85, 43), (slider_x_brightness, slider_y_brightness, slider_width, slider_height))
    pygame.draw.circle(screen, (184, 184, 148), (knob_x_brightness, slider_y_brightness + slider_height // 2), knob_radius)



def draw_maze():
    # Initialising maze
    screen.blit(game_screen, (0, 0))
    maze_x_offset = 300  # Shift maze to the right slightly
    maze_y_offset = 205  # Shift maze down slightly
    Cell_Size = 55
    maze_width = 600
    maze_height = 600
    pygame.draw.rect(screen, (222,184,135), (305, maze_y_offset, maze_width, maze_height))

    # Initialising grass
    grass.convert_alpha()
    bush = pygame.transform.scale(grass, (Cell_Size, Cell_Size))

    # Initialising player
    x_offset = (Width - (Cell_Size*Cols))//2
    player_size = Cell_Size // 2
    player_offset = (Cell_Size - player_size) // 2  # centers the player in the cell

    # draw the maze
    for row in range(Rows - 1):
        for col in range(Cols - 1):
            x, y = maze_x_offset + col * Cell_Size, maze_y_offset + row * Cell_Size
            if maze[row][col] == 1:
                screen.blit(bush, (x, y))


    #Draw collectible bone
    collectible_x = 50 + x_offset + collectible_col * Cell_Size + player_offset
    collectible_y = maze_y_offset + collectible_row * Cell_Size + player_offset
    screen.blit(bone, (collectible_x - 20, collectible_y - 5))

    # Draw player
    player_x = 50 + x_offset + player_col * Cell_Size + player_offset
    player_y = maze_y_offset + player_row * Cell_Size + player_offset
    screen.blit(character, (player_x - 20, player_y - 25))


    # Draw bone counter
    Bone_text = (pygame.font.Font(None, 50)).render(f"{Bone_count}", True, (222,184,135))
    screen.blit(Bone_text, (250, 250))

    # Back button
    screen.blit(back_button, back_button_position.topleft)

    # Colour blind button
    screen.blit(colour_blind_button, colour_blind_button_position.topleft)

    # Draw touch controls
    screen.blit(up_arrow, up_arrow_position.topleft)
    screen.blit(down_arrow, down_arrow_position.topleft)
    screen.blit(left_arrow, left_arrow_position.topleft)
    screen.blit(right_arrow, right_arrow_position.topleft)

shine_scale = 1.3  # Initial scale (1.0 = original size)
scale_direction = 0.0065  # Speed of scaling (adjust for faster/slower effect)


def Generate_The_Maze(x, y):
    maze[y][x] = 0
    random.shuffle(Directions)


    for dx, dy in Directions:
        print(f"Generating maze at {x}, {y}")
        nx, ny = x+ dx, y + dy
        if 0< ny < Rows-1 and 0 < nx < Cols-1 and maze[ny][nx] == 1:
            maze[y + dy//2][x + dx//2] = 0
            Generate_The_Maze(nx, ny)

Generate_The_Maze(1, 1)

collectible_row, collectible_col = get_random_maze_position()



def draw_completion_screen():
    screen.blit(completion_screen, (0, 0))
    screen.blit(home_button, home_button_position.topleft)
    screen.blit(information_button, information_button_position.topleft)

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

arrow_y_offset = 0
arrow_direction = 1
arrow_speed = 0.25

def draw_information_screen():
    global arrow_y_offset, arrow_direction
    screen.blit(information_screen, (0, 0))
    screen.blit(home_button, home_button_position.topleft)

    arrow_y_offset += arrow_direction * arrow_speed

    if arrow_y_offset >= 15 or arrow_y_offset <= 0:
        arrow_direction *= -1

    screen.blit(conversion_arrow, (conversion_arrow_position.x, conversion_arrow_position.y + arrow_y_offset))

def Move_player(dx, dy):
    global player_row, player_col, collectible_col, collectible_row, Bone_count
    new_row = player_row + dy
    new_col = player_col + dx

    #check movement is allowed, not into a wall
    if 0 <= new_row < Rows and 0 <= new_col < Cols and maze[new_row][new_col] == 0:
        player_row, player_col = new_row, new_col

        if player_row == collectible_row and player_col == collectible_col:
            Bone_count +=1
            collectible_row, collectible_col = get_random_maze_position() # spawn a new item

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
    elif game_state == 'information':
        draw_information_screen()
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
            elif game_state == 'game':
                if up_arrow_position.collidepoint(mouse_pos):
                    Move_player(0, -1)
                elif down_arrow_position.collidepoint(mouse_pos):
                    Move_player(0, 1)
                elif left_arrow_position.collidepoint(mouse_pos):
                    Move_player(-1, 0)
                elif right_arrow_position.collidepoint(mouse_pos):
                    Move_player(1, 0)
                elif back_button_position.collidepoint(mouse_pos):
                    game_state = 'menu'
                elif colour_blind_button_position.collidepoint(mouse_pos):
                    overlay = pygame.Surface((button_width * 0.75, button_height * 0.75), pygame.SRCALPHA)
                    overlay.fill((0, 153, 0, 51))  # Green overlay
                    screen.blit(colour_blind_button, colour_blind_button_position.topleft)
                    screen.blit(overlay, colour_blind_button_position.topleft)
                    pygame.display.flip()
                    pygame.time.delay(150)
            elif game_state in ['instructions']:
                if back_button_position.collidepoint(mouse_pos):
                    game_state = 'menu'
            elif game_state == 'complete':
                if home_button_position.collidepoint(mouse_pos):
                    game_state = 'menu'
                elif information_button_position.collidepoint(mouse_pos):
                    overlay = pygame.Surface((button_width * 0.75, button_height * 0.75), pygame.SRCALPHA)
                    overlay.fill((0, 153, 0, 51))  # Green overlay
                    screen.blit(information_button, information_button_position.topleft)
                    screen.blit(overlay, information_button_position.topleft)
                    pygame.display.flip()
                    pygame.time.delay(150)
                    game_state = 'information'
            elif game_state == 'settings':
                # Check if user clicked volume knob
                if (knob_x_volume - knob_radius <= mouse_x <= knob_x_volume + knob_radius and
                        slider_y_volume - knob_radius <= mouse_y <= slider_y_volume + slider_height + knob_radius):
                    is_dragging_volume = True
                # Check if user clicked brightness knob
                if (knob_x_brightness - knob_radius <= mouse_x <= knob_x_brightness + knob_radius and
                        slider_y_brightness - knob_radius <= mouse_y <= slider_y_brightness + slider_height + knob_radius):
                    is_dragging_brightness = True
                elif back_button_position.collidepoint(mouse_pos):
                    game_state = 'menu'
            elif game_state == 'information':
                if home_button_position.collidepoint(mouse_pos):
                    game_state = 'menu'
        elif event.type == pygame.MOUSEBUTTONUP:
            if game_state == 'settings':
                is_dragging_volume = False
                is_dragging_brightness = False

        elif event.type == pygame.MOUSEMOTION:
            if game_state == 'settings':
                mouse_x, mouse_y = event.pos
                # Move volume slider
                if is_dragging_volume:
                    knob_x_volume = max(slider_x_volume, min(mouse_x, slider_x_volume + slider_width))
                    volume = (knob_x_volume - slider_x_volume) / slider_width  # Normalize between 0 and 1
                # Move brightness slider
                if is_dragging_brightness:
                    knob_x_brightness = max(slider_x_volume, min(mouse_x, slider_x_volume + slider_width))
                    brightness = (knob_x_brightness - slider_x_brightness) / slider_width  # Normalize between 0 and 1

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