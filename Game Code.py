import pygame
from pygame.locals import *
import random

# Initialises pygame
pygame.init()

# Screen images
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

# Defining button dimensions and spacings
button_x = (Width - button_width) // 2
button_spacing = 20  # The space between the buttons

# Defining button positions
play_button_position = play_button.get_rect(topleft=(button_x, 300))
instructions_button_position = instructions_button.get_rect(topleft=(button_x, play_button_position.bottom + button_spacing))
settings_button_position = settings_button.get_rect(topleft=(button_x, instructions_button_position.bottom + button_spacing))
back_button_position = back_button.get_rect(bottomleft=(-35, Height - 20))

Bone_count = 0
Bone_font = pygame.font.Font(None, 25)
bone_colour = (0,255,0)

pathcolour = (222,184,135)

white = (255, 255, 255)
black = (1,1,1)
red = (255,0,0)
gray = (100,100,100)

Cell_Size = 80 #best for the grid to fit the height

Rows, Cols = 10, 10

x_offset = (Width - (Cell_Size*Cols))//2

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


grass.convert_alpha()
bush = pygame.transform.scale(grass, (Cell_Size, Cell_Size))

player_row, player_col = 1, 1

player_size = Cell_Size // 2
player_offset = (Cell_Size - player_size) //2 #centers the player in the cell

small_font = pygame.font.Font(None, 50)

#game state
game_state = "menu"

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
    screen.fill(pathcolour)  # fills the background

    # draw the maze
    for row in range(Rows):
        for col in range(Cols):
            x, y = x_offset + col * Cell_Size, row * Cell_Size
            if MazeGrid[row][col] == 1:
                screen.blit(bush, (x, y))

    collectible_x = x_offset + collectible_col * Cell_Size + player_offset
    collectible_y = collectible_row * Cell_Size +player_offset
    pygame.draw.circle(screen, bone_colour, (collectible_x + player_size // 2, collectible_y+ player_size // 2), player_size //3)

    #draw the player
    player_x = x_offset + player_col * Cell_Size + player_offset
    player_y = player_row * Cell_Size + player_offset
    pygame.draw.rect(screen, red, (player_x, player_y, player_size, player_size))

    Bone_text = small_font.render(f"bones: {Bone_count}", True, black)
    screen.blit(Bone_text, (10,10))

    #if 10 bones are collected the information page is shown

slider_x = 200
slider_y = 500
slider_width = 400
slider_height = 10
knob_radius = 10
knob_x = slider_x + slider_width // 2  # Start in the middle
brightness = 1.0  # 1.0 = normal, <1.0 = darker


def draw_completion_screen():
    screen.blit(skeleton, (0, 0))#create an image of size 800x800 i think

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
                    game_state = 'game'
                elif instructions_button_position.collidepoint(mouse_pos):
                    game_state = 'instructions'
                elif settings_button_position.collidepoint(mouse_pos):
                    game_state = 'settings'
            elif game_state in ['instructions', 'settings']:
                if back_button_position.collidepoint(mouse_pos):
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