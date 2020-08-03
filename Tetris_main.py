import pygame
import random

from pygame import mixer

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()
pygame.mixer.init()
mixer.music.load('320232__foolboymedia__video-game-land.wav')
mixer.music.play(-1)

# GLOBAL VARIABLES
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2  # 250
top_left_y = s_height - play_height  # 100

# SHAPE FORMATS

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',  # (line -> .....) enumarate 0, .....(line)
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


# index 0 - 6 predstavlja shape


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


# PRAVI KOCKICE NA EKRANU, a draw grid CRTA LINIJE IZMEDJU KOCKICA
def create_grid(locked_positions={}):  # definisemo sta je grid i deminezije 10x20 i BOJE(lokovane pozicije)
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]  # boja kockica na igralistu:::: sve su crne
    ### grid = [[(0,0,0), (0,0,0), (0,0,0), (0,0,0).....deseti (0,0,0)], [(0,0,0), (0,0,0)...jos osam]...jos 8 lista]

    # POPUNJAVA BOJE NA GRID-U
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:  # samo provera npr. dictionary """""""(1, 1): (255, 0, 0)"""""""""""
                c = locked_positions[(j, i)]  # key for dictionary above
                grid[i][j] = c  # ako jeste dodaje kockici tu boju

    return grid  ### ovaj grid ide u valid space


def convert_shape_format(shape):  # najkomplikovanija funk, konvertuje tacke i nule u oblike, koji ce da padaju sa vrha
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]  # format = list that contains 0 and .

    for i, line in enumerate(format):
        row = list(line)  # row = [., ., ., ., .] ; i = 0 |||  row = [., ., 0, ., .] ; i=1 ||||
        for j, column in enumerate(row):  # . ; j=0|||  . ; j=1||| . ; j=2||| . ; j=3||| . ; j=4||||||||||||| i =0
            if column == "0":
                positions.append((shape.x + j, shape.y + i))

    # da kada oblik krene da pada, bude van ekrana, pa polako pada ka dole
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):  # if grid[i][j] == (0, 0, 0) this check is there any color in there (is it empty?)
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]  # [[(2,3)],[(1, 4)]]
    accepted_pos = [j for sub in accepted_pos for j in sub]  # [(2,3),(1, 4)]

    formatted = convert_shape_format(shape)  # [(1,3),(3, 4)]

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:  # pos[1] is y axis, -1 means it is out of the screen, and we dont want to check those
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def get_shape():  # bira nasumican oblik iz liste shapes i vraca ga kao klasu
    return Piece(5, 2, random.choice(shapes))


def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (
        top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - label.get_height() / 2))


def draw_grid(surface, grid):  # CRTAMO(draw) 20 horizontalnih i 10 uspravnih linija
    sx = top_left_x  # start x, to make things shorter so we dont have to type top_left_x
    sy = top_left_y

    for i in range(len(grid)):  # (128,128,128) GREY
        # horizontal lines
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * block_size), (sx + play_width, sy + i * block_size))
        for j in range(len(grid[i])):
            # vertical lines
            pygame.draw.line(surface, (128, 128, 128), (sx + j * 30, sy), (sx + j * 30, sy + play_height))


def clear_rows(grid, locked, surface):
    deleted_rows = []
    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        # idemo od nazad od 19,18.....0  19 je prvi dole red
        row = grid[i]
        if (0, 0, 0) not in row:  # """"""" (1, 1): (255, 0, 0)""""""""""" locked postion
            inc += 1
            # index_row= i  # index reda (broj reda)
            for j in range(len(row)):
                del locked[(j, i)]# brise popunjen red
            deleted_rows.append(i)

    if len(deleted_rows) == 1 or len(deleted_rows) == 4:
        for key in sorted(list(locked), key=lambda x: x[1], reverse=True):
            x, y = key
            if y < deleted_rows[0]:
                newKey = (x, y + len(deleted_rows))
                locked[newKey] = locked.pop(key)
    elif len(deleted_rows) == 2:
        for key in sorted(list(locked), key=lambda x: x[1], reverse=True):
            x, y = key
            if y < deleted_rows[0] and y > deleted_rows[1]:
                newKey = (x, y + 1)
                locked[newKey] = locked.pop(key)
            elif y < deleted_rows[1]:
                newKey = (x, y + 2)
                locked[newKey] = locked.pop(key)
    elif len(deleted_rows) == 3:
        for key in sorted(list(locked), key=lambda x: x[1], reverse=True):
            x, y = key
            if y < deleted_rows[0] and y > deleted_rows[1]:
                newKey = (x, y + 1)
                locked[newKey] = locked.pop(key)
            elif y < deleted_rows[1] and y > deleted_rows[2]:
                newKey = (x, y + 2)
                locked[newKey] = locked.pop(key)
            elif y < deleted_rows[2]:
                newKey = (x, y + 3)
                locked[newKey] = locked.pop(key)

    if inc == 0:
        return inc
    if inc == 1:
        sound1 = mixer.Sound('109662__grunz__success.wav')
        sound1.set_volume(10)
        sound1.play()
        return inc  # da vidimo sa koliko mnozimo skor, ako je inc 3, tri reda smo spojili, score = 3*10
    if inc == 2:
        sound1 = mixer.Sound('109662__grunz__success.wav')
        sound1.set_volume(10)
        sound1.play()

        font = pygame.font.SysFont('comicsans', 40, bold=True)
        label3 = font.render("BONUS POINTS FOR GRIFINDORRR!", 1, (255, 255, 255))
        surface.blit(label3, (top_left_x - 120, top_left_y - 30))
        pygame.display.update()
        pygame.time.delay(1000)
        return int(3)
    if inc == 3:
        sound1 = mixer.Sound('109662__grunz__success.wav')
        sound1.set_volume(10)
        sound1.play()

        font = pygame.font.SysFont('comicsans', 40, bold=True)
        label3 = font.render("BONUS POINTS FOR GRIFINDORRR!", 1, (255, 255, 255))
        surface.blit(label3, (top_left_x - 120, top_left_y - 30))
        pygame.display.update()
        pygame.time.delay(1000)
        return int(5)
    if inc == 4:
        sound1 = mixer.Sound('109662__grunz__success.wav')
        sound1.set_volume(10)
        sound1.play()

        font = pygame.font.SysFont('comicsans', 40, bold=True)
        label3 = font.render("BONUS POINTS FOR GRIFINDORRR!", 1, (255, 255, 255))
        surface.blit(label3, (top_left_x - 120, top_left_y - 30))
        pygame.display.update()
        pygame.time.delay(1000)
        return int(10)


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30, bold=True)
    label = font.render('Next piece', 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + 100

    format = shape.shape[shape.rotation % len(shape.shape)]

    # crta kvadrat na kojem ce biti sledeci oblik
    pygame.draw.rect(surface, (10, 0, 150), (sx - 10, sy - 20, 180, 180), 0)

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == "0":  # provera u originalnim listama u svakom redu da li postoji nula i onda iscrtava
                pygame.draw.rect(surface, shape.color, (sx + j * 30, sy + i * 30, 30, 30), 0)

    # crta crnikvadrat oko sledeceg oblika
    pygame.draw.rect(surface, (0, 0, 0), (sx - 10, sy - 20, 180, 180), 4)

    # ispisuje tekst Next piece
    surface.blit(label, (sx + 20, sy - 50))


def draw_window(surface, grid, score=0, highscore=0):
    surface.fill((0, 200, 0))

    pygame.font.init()
    font = pygame.font.SysFont("comicsans", 60, bold=True)
    label = font.render("Tetris", 1, (230, 0, 200))

    surface.blit(label, (top_left_x + play_width / 2 - label.get_width() / 2, 30))

    # za score
    font = pygame.font.SysFont('comicsans', 30, bold=True)
    label1 = font.render('Score: ' + str(score), 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + 100
    surface.blit(label1, (sx + 40, sy + 200))

    # za highscore i poene##########################

    label2 = font.render('Highscore: ' + highscore, 1, (255, 255, 255))

    surface.blit(label2, (top_left_x - 220, top_left_y + 300))

    label3 = font.render("1 row = 10 points", 1, (255, 255, 255))
    surface.blit(label3, (top_left_x - 240, top_left_y + 350))
    label4 = font.render("2 rows = 30 points", 1, (255, 255, 255))
    surface.blit(label4, (top_left_x - 240, top_left_y + 370))
    label5 = font.render("3 rows = 50 points", 1, (255, 255, 255))
    surface.blit(label5, (top_left_x - 240, top_left_y + 390))
    label6 = font.render("4 rows = 100 points", 1, (255, 255, 255))
    surface.blit(label6, (top_left_x - 240, top_left_y + 410))

    for i in range(len(grid)):  # CRTA IGRALISTE ALOOOOOO
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * block_size, top_left_y + i * 30, 30, 30), 0)

    # crta CRVENI PRAVOUGANIK OKO IGRALISTA
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 4)

    draw_grid(surface, grid)  # crta vodoravne i uspravne sive linije (128,128,128)
    ###########pygame.display.update() ne treba ovde negu u mainu


def update_score(highscore):
    score = max_score()

    q = open("scores.txt", "w")
    if int(score) > highscore:
        q.write(str(score))
    else:
        q.write(str(highscore))


def max_score():
    with open("scores.txt", "r") as f:
        lines = f.readline()
        score = lines.strip()

    return score
def make_locked():
    dict={}
    for row in range(19,15,-1):
        for column in range(0,9):
            if (row == 17 and column == 5):
                continue
            dict[(column,row)] = (255,0,0)
    return dict

def main(win):
    highscore = max_score()
    locked_positions = make_locked()

    change_piece = False
    run = True  # for while loop

    current_piece = Piece(9,7,shapes[2])
    next_piece = get_shape()

    clock = pygame.time.Clock()  ####clock object
    fall_time = 0
    level_time = 0
    score = 0
    fall_speed = 0.3
    while run:

        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time / 1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.01

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True
        ####################################POMERANJE LEVO DESNO ########
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            current_piece.x -= 1
            pygame.time.delay(120)
            if not (valid_space(current_piece, grid)):
                current_piece.x += 1
        if keys[pygame.K_RIGHT]:
            current_piece.x += 1
            pygame.time.delay(120)
            if not (valid_space(current_piece, grid)):
                current_piece.x -= 1
        ################################################################

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.y -= 1

                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.rotation -= 1

                if event.key == pygame.K_SPACE:
                    fall_speed = 0.01

            if event.type == pygame.KEYUP:
                fall_speed = 0.3

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:  #############################################pravi LOKOVANE KVADRATICE I PUSTA SLEDECI OBLIK
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

            score += clear_rows(grid, locked_positions, win) * 10

        draw_window(win, grid, score, highscore)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            sound1 = mixer.Sound('483058__mattiagiovanetti__arcade-death-theme.wav')
            sound1.set_volume(10)
            sound1.play()
            draw_text_middle(win, "YOU LOSE", 100, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(3500)
            run = False
            update_score(score)


def main_menu(win):
    run = True
    while run:

        win.fill((0, 0, 0))
        draw_text_middle(win, "Press any key to play", 60, (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.display.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(win)  # start game