#importing all modules
import pygame#pip install pygame
from pygame.locals import *
import random
from pygame import mixer
  
#initiating modules needed
pygame.init()
mixer.init()
pygame.font.init()

#variables
s_width = 900
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per blo ck
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

backimg = pygame.image.load("space.png")



#shapes for game
Tri =[['.....',
      '..0..',
      '.000.',
      '00000',
      '.....'],
     ['.....',
      '0....',
      '000..',
      '00000',
      '.....'],
     ['.....',
      '.....',
      '00000',
      '.000.',
      '..0..'],
     ['.....',
      '....0',
      '..000',
      '00000',
      '.....']]

Cir = [['.....',
        '.00..',
        '0000',
        '0000.',
        '.00..',]]
       

line = [['0....',
      '0....',
      '0....',
      '0....',
      '0....'],
      ['0000.',
       '.....',
       '.....',
       '.....',
       '.....',]]


       
slin = [['0....',
         '.0..',
         '..0..',
         '...0.',
         '....0'],
        ['....0',
         '...0.',
         '..0..',
         '.0...',
         '0....']]

dia = [['..0..',
        '.000.',
        '00000',
        '.000.',
        '..0..']]

smol = [['.....',
        '.....',
        '..0..',
        '.....',
        '.....']]

ryu = [['.....',
        '.....',
        '00000',
        '..0..',
        '.....'],
       ['....0',
        '....0',
        '...00',
        '....0',
        '....0'],
       ['0....',
        '0....',
        '00...',
        '0....',
        '0....'],
       ['.....',
        '..0..',
        '00000',
        '.....',
        '.....']]

remp = [['0....',
         '.0...',
         '..0..',
         '.0...',
         '0....'],
        ['....0',
         '...0.',
         '..0..',
         '...0.',
         '....0',],
        ['.....',
         '.....',
         '0...0',
         '.0.0.',
         '..0..'],
        ['.....',
         '.....',
         '..0..',
         '.0.0.',
         '0...0']]

sss = [['.....',
        '..00.',
        '..0..',     
        '..0..',
        '.00..'],
        ['.....',
         '.00..',
         '..0..',
         '..0..',
         '..00.'],
       ['.....',
        '.....',
        '0....',
        '00000',
        '....0'],
       ['.....',
        '.....',
        '....0',
        '00000',
        '0....']]


shapes = [Tri, Cir, line, slin, dia, smol, ryu, remp, sss]
shape_colors = [(0, 102, 0), (255, 0, 0), (225, 128, 0), (255, 255, 0), (250, 200, 150), (10, 255, 200), (210, 0, 242), (82, 255, 158), (96, 96, 96)]


#defining the gam pieces
class Piece(object):

    rows = 20  # y
    columns = 10  # x

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  
#creating game grid
def create_grid(locked_positions={}):
    grid = [[(0,0,0) for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
    return grid

#onverting the shape format
def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

#checks spaces
def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False

    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

#chooses a random shape
def get_shape():
    global shapes, shape_colors

    return Piece(5, 0, random.choice(shapes))

#draw text in the middle of the screen
def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width() / 2), top_left_y + play_height/2 - label.get_height()/2))

#draw the grid
def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (128,128,128), (sx, sy+ i*30), (sx + play_width, sy + i * 30))  # horizontal lines
        for j in range(col):
            pygame.draw.line(surface, (128,128,128), (sx + j * 30, sy), (sx + j * 30, sy + play_height))  # vertical lines

#clear the rows after fully overed
def clear_rows(grid, locked):
    # need to see if row is clear the shift every other row above down one

    inc = 0
    for i in range(len(grid)-1,-1,-1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            # add positions to remove from locked
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

#show next shape in corner
def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*30, sy + i*30, 30, 30), 0)

    surface.blit(label, (sx + 10, sy- 30))
#background 
def draw_window(surface):
    win.blit(backimg, backimg.get_rect())
    font = pygame.font.SysFont('arialblack', 60)
    label = font.render('ALTERISS', 1, (255,255,255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j* 30, top_left_y + i * 30, 30, 30), 0)

    # draw grid and border
    draw_grid(surface, 20, 10)
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)
    # pygame.display.update()
#play music
def music_play():
    mixer.music.load("Crazy - Patrick Patrikios.mp3")
  

    mixer.music.set_volume(0.7)
  
 
    mixer.music.play()
  
#main game loop
def main():
    global grid

    locked_positions = {}  # (x,y):(255,0,0)
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0

    while run:
        fall_speed = 0.27

        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        # PIECE FALLING CODE
        if fall_time/1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_UP:
                    # rotate shape
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

                if event.key == pygame.K_DOWN:
                    # move shape down
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

        shape_pos = convert_shape_format(current_piece)

        # add piece to the grid for drawing
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # IF PIECE HIT GROUND
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

            # call four times to check for multiple clear rows
            clear_rows(grid, locked_positions)

        draw_window(win)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        # Check if user lost
        if check_lost(locked_positions):
            run = False

            draw_text_middle("You Lost", 40, (255,255,255), win)
            pygame.display.update()
            pygame.time.delay(2000)
            

#main menu
def main_menu():
    run = True
    while run:
        win.fill((0,0,0))
        draw_text_middle('''Made by Avanindra Chakraborty for AISC COTW 7,  click enter to start
Controls: LEFT, RIGHT KEYS TO MOVE, UP TO CHANGE''', 18, (255, 255, 255), win)
        draw_text_middle('', 28, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                #music_play()
                main()
                
    pygame.quit()


win = pygame.display.set_mode((s_width, s_height), RESIZABLE, 32)
pygame.display.set_caption('Tetris')

main_menu()  # start game
