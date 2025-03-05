import pygame
from pygame.locals import *
import random

#initialise pygame
pygame.init()

Bone_count = 0
Bone_font = pygame.font.Font(None, 25)

DinoImage = pygame.image.load(('hi'))

bone_colour = (0,255,0)

pathcolour = (222,184,135)

white = (255, 255, 255)
black = (1,1,1)
red = (255,0,0)
gray = (100,100,100)

Width, Height = 800, 800


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


pygame.display.set_caption("Maze Game")
screen = pygame.display.set_mode((Width, Height))

bush = pygame.image.load('').convert_alpha()
bush = pygame.transform.scale(bush, (Cell_Size, Cell_Size))

#surface = pygame.display.set_mode((400, 300))


font = pygame.font.Font(None, 100)#large text for menu
small_font = pygame.font.Font(None, 50)

player_row, player_col = 1, 1

player_size = Cell_Size // 2
player_offset = (Cell_Size - player_size) //2 #centers the player in the cell


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
    screen.fill(white)

    title= font.render("Maze Game", True, black)
    Start_text = font.render("press ENTER to start", True, black)

    title_x = (Width - title.get_width())// 2
    title_y = (Height // 3)

    start_x = (Width - Start_text.get_width()) // 2
    start_y = title_y + 200

    #draw text

    screen.blit(title, (title_x, title_y))
    screen.blit(Start_text, (start_x, start_y))

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


#def adjust_brightness(image, brightness):
#    img_copy = image.copy()
#    img_copy.fill((brightness * 255, brightness *255, brightness *255), special_flags=pygame.BLEND_MULT)
#    return img_copy
#def draw_settings():
#    screen.fill(pathcolour)
#    pygame.draw.rect(screen, gray(slider_x, slider_y, slider_width, slider_height))
#    pygame.draw.circle((screen, red(knob_x, slider_y + slider_height // 2), knob_radius))

#    print("settings")
     #create a page with sliders to adjust the brightness

def draw_info():
    screen.blit(DinoImage, (0, 0))#create an image of size 800x800 i think

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
    screen.fill(pathcolour)

    #bright_image = adjust_brightness(DinoImage, brightness)
    #screen.blit(bright_image, (100, 100))

    if Bone_count == 10:
        #print("end")
        game_state = "info"
        Bone_count = 0
        #print(game_state)

    # controls the event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif game_state == "menu" and event.key == K_RETURN:
                game_state = "game"
            elif event.key == K_LALT:
                game_state= "settings"
            elif event.key == K_RETURN and game_state == "info":
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
                    game_state == "info"
                #elif event.key == K_b:
                #    game_state == "settings"


    if game_state == "menu":
        draw_menu()
    elif game_state == "game":
        draw_maze()
    elif game_state == "info":
        draw_info()
    #elif game_state == "settings":
    #    draw_settings()
    pygame.display.flip()  # updates the display


pygame.quit()