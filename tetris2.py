import os
import pygame
import sys
import schedule
import random

os.system("cls")
pygame.init()

dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir)

def first_setting():
    
    global yline_num, xline_num, one_pixel_size, White_space, selcet
    xline_num = 10+2          ## X라인 개수
    yline_num = 20+2          ## Y라인 개수
    White_space = 5
    one_pixel_size = 30
    selcet = 1

    global tile_map, move_map, test_count40, time_count, done, screen, clock, y_line_down, move_figure, x_line_side, move_close_left, move_close_right, background_num, next_result, next_tile_map
    size = [(xline_num*one_pixel_size)+(White_space*2)+150, (yline_num*one_pixel_size)+(White_space*2)]
    done = False
    screen = pygame.display.set_mode(size)
    screen.fill([0,0,0])
    clock = pygame.time.Clock()
    time_count = 40
    test_count40 = 0
    next_tile_map = []
    tile_map = []
    move_map = []
    y_line_down = 1
    x_line_side = 4
    move_figure = 0
    move_close_left = 0
    move_close_right = 0
    background_num = 0
    next_result = 9
    
    global figure_num, figure_shape, figure_num_direction1, figure_num_direction2, figure_num_direction3
    figure_num =[0,1,2,3,4,5,6]
    figure_num_direction1 =[0,1,2,3]
    figure_num_direction2 =[0,1,2]
    figure_num_direction3 =[0,1]
    # figure_shape =[모양[돌림x4[y열[x열]]]]
    figure_shape = [[
        [[0,0,1,0], 
         [0,0,1,0], 
         [0,0,1,0], 
         [0,0,1,0]],
        [[0,0,0,0], 
         [0,0,0,0], 
         [1,1,1,1], 
         [0,0,0,0]],
        [[0,0,1,0], 
         [0,0,1,0], 
         [0,0,1,0], 
         [0,0,1,0]],
        [[0,0,0,0], 
         [0,0,0,0], 
         [1,1,1,1], 
         [0,0,0,0]]],
                    
        [[[0,2,0], 
         [0,2,0], 
         [0,2,2]],
        [[0,0,0],   
         [2,2,2], 
         [2,0,0]],
        [[2,2,0],   
         [0,2,0], 
         [0,2,0]],
        [[0,0,2],   
         [2,2,2], 
         [0,0,0]]],
        
        [[[0,3,0], 
         [0,3,0], 
         [3,3,0]],
        [[3,0,0],   
         [3,3,3], 
         [0,0,0]],
        [[0,3,3],   
         [0,3,0], 
         [0,3,0]],
        [[0,0,0],   
         [3,3,3], 
         [0,0,3]]],
        
        [[[0,0,0], 
         [0,4,4], 
         [4,4,0]],
        [[0,4,0],   
         [0,4,4], 
         [0,0,4]],
        [[0,0,0],   
         [0,4,4], 
         [4,4,0]],
        [[0,4,0],   
         [0,4,4], 
         [0,0,4]]],
        
        [[[0,0,0], 
         [5,5,0], 
         [0,5,5]],
        [[0,5,0],   
         [5,5,0], 
         [5,0,0]],
        [[0,0,0],   
         [5,5,0], 
         [0,5,5]],
        [[0,5,0],   
         [5,5,0], 
         [5,0,0]]],
        
        [[[0,6,0], 
         [6,6,6], 
         [0,0,0]],
        [[0,6,0],   
         [0,6,6], 
         [0,6,0]],
        [[0,0,0],   
         [6,6,6], 
         [0,6,0]],
        [[0,6,0],   
         [6,6,0], 
         [0,6,0]]],
        
        [[[7,7], 
         [7,7]],
        [[7,7], 
         [7,7]],
        [[7,7], 
         [7,7]],
        [[7,7], 
         [7,7]]]]

    global background, tetris_1, tetris_2, tetris_3, tetris_4 , tetris_5 , tetris_6 , tetris_7, tetris_8, tetris_9        # 기초 배치 이미지
    background = pygame.transform.scale(pygame.image.load('image/tetris_start_background.jpg'), ((xline_num*one_pixel_size)+(White_space*2)+150, (yline_num*one_pixel_size)+(White_space*2)))
    tetris_1 = pygame.transform.scale(pygame.image.load('image/teteris_1.png'), (one_pixel_size - 2, one_pixel_size - 2))
    tetris_2 = pygame.transform.scale(pygame.image.load('image/teteris_2.png'), (one_pixel_size - 2, one_pixel_size - 2))
    tetris_3 = pygame.transform.scale(pygame.image.load('image/teteris_3.png'), (one_pixel_size - 2, one_pixel_size - 2))
    tetris_4 = pygame.transform.scale(pygame.image.load('image/teteris_4.png'), (one_pixel_size - 2, one_pixel_size - 2))
    tetris_5 = pygame.transform.scale(pygame.image.load('image/teteris_5.png'), (one_pixel_size - 2, one_pixel_size - 2))
    tetris_6 = pygame.transform.scale(pygame.image.load('image/teteris_6.png'), (one_pixel_size - 2, one_pixel_size - 2))
    tetris_7 = pygame.transform.scale(pygame.image.load('image/teteris_7.png'), (one_pixel_size - 2, one_pixel_size - 2))
    tetris_8 = pygame.transform.scale(pygame.image.load('image/teteris_8.jpg'), (one_pixel_size - 2, one_pixel_size - 2))
    tetris_9 = pygame.transform.scale(pygame.image.load('image/teteris_9.jpg'), (one_pixel_size - 2, one_pixel_size - 2))
    
    global font
    font_size = 40
    font = pygame.font.SysFont(None,font_size)
first_setting()

def sceond_setting():
    global level, score, lines, experience
    level = 1
    score = 0
    lines = 0
    experience = 0
sceond_setting()

def change_score():
    global view_level, view_score, view_lines
    view_level = font.render(str(level),True,(255,255,255))
    view_score = font.render(str(score),True,(255,255,255))
    view_lines = font.render(str(lines),True,(255,255,255))
change_score()

def help_massage():
    global message1, message2, message3, message4
    message1 = font.render("NEXT",True,(255,255,255))
    message2 = font.render("LEVEL",True,(255,150,150))
    message3 = font.render("SCORE",True,(50,255,100))
    message4 = font.render("LINES",True,(0,255,255))
help_massage()   

def make_tile_map():
    tile_map.clear()
    for yline in range(yline_num):
        etc_map = []
        for xline in range(xline_num):
            etc_map.append(0)
        tile_map.append(0)
        tile_map[yline] = etc_map
    tile_map[0] = [9,9,9,9,9,9,9,9,9,9,9,9]
    for a in range(1,22):
        tile_map[a] = [9,0,0,0,0,0,0,0,0,0,0,9]
    tile_map[21] = [9,9,9,9,9,9,9,9,9,9,9,9]
make_tile_map()

def make_move_map():
    move_map.clear()
    for yline in range(yline_num):
        etc2_map = []
        for xline in range(xline_num):
            etc2_map.append(0)
        move_map.append(0)
        move_map[yline] = etc2_map
    move_map[0] = [9,9,9,9,9,9,9,9,9,9,9,9]
    for a in range(1,22):
        move_map[a] = [9,0,0,0,0,0,0,0,0,0,0,9]
    move_map[21] = [9,9,9,9,9,9,9,9,9,9,9,9]
make_move_map()

def view_terminal_map():
    global selcet
    for yline in range(yline_num):
        for xline in range(xline_num):
            if selcet == 1 : print(tile_map[yline][xline], end=' ')
            if selcet == 2 : print(move_map[yline][xline], end=' ')
        print()
view_terminal_map()

def view_help_message():
    pygame.draw.rect(screen,[0,0,0]   ,(370 , 20,140,170))
    pygame.draw.rect(screen,[50,50,50],(370 , 20,140,170),3)
    screen.blit(message1, (400, 30))
    screen.blit(message2, (398, 210))
    screen.blit(message3, (392, 280))
    screen.blit(message4, (400, 350))
view_help_message()

def view_change_score():
    global view_level, view_score, view_lines
    pygame.draw.rect(screen,[0,0,0] ,(420, 242, 60, 30))
    pygame.draw.rect(screen,[0,0,0] ,(420, 312, 70, 30))
    pygame.draw.rect(screen,[0,0,0] ,(400, 382, 80, 30))
    if level <  10                    : screen.blit(view_level, (433, 242))
    if level >= 10                    : screen.blit(view_level, (425, 242))
    if score <  10                    : screen.blit(view_score, (433, 312))
    if score >= 10   and score < 100  : screen.blit(view_score, (425, 312))
    if score >= 100  and score < 1000 : screen.blit(view_score, (417, 312))
    if score >= 1000                  : screen.blit(view_score, (409, 312))
    screen.blit(view_lines, (433, 382))
view_change_score()

def view_next_shape():
    next_tile_map.clear()
    for num in range(3):
        if len(figure_shape[next_result][next_result2][0]) == num + 2 : 
            for yline in range(num + 2):
                etc3_map = []
                for xline in range(num + 2):
                    etc3_map.append(figure_shape[next_result][next_result2][yline][xline])
                next_tile_map.append(0)
                next_tile_map[yline] = etc3_map
        if len(next_tile_map) == num + 2 : 
            if num + 2 == 4 : width, height = 376, 56
            if num + 2 == 3 : width, height = 390, 70
            if num + 2 == 2 : width, height = 405, 83
            for yline in range(num + 2):
                for xline in range(num + 2):
                    ########## 배경을 넣을까 말까 고민중
                    # if next_tile_map[yline][xline] == 0 :
                    #     pygame.draw.rect(screen,[20,20,20], (((one_pixel_size * xline) + White_space)+width, (one_pixel_size * yline) + White_space+height, one_pixel_size - 2,one_pixel_size - 2))
                    if next_tile_map[yline][xline] == 1 : screen.blit(tetris_1,((xline*one_pixel_size) + White_space+width,(yline*one_pixel_size) + White_space+height))
                    if next_tile_map[yline][xline] == 2 : screen.blit(tetris_2,((xline*one_pixel_size) + White_space+width,(yline*one_pixel_size) + White_space+height))
                    if next_tile_map[yline][xline] == 3 : screen.blit(tetris_3,((xline*one_pixel_size) + White_space+width,(yline*one_pixel_size) + White_space+height))
                    if next_tile_map[yline][xline] == 4 : screen.blit(tetris_4,((xline*one_pixel_size) + White_space+width,(yline*one_pixel_size) + White_space+height))
                    if next_tile_map[yline][xline] == 5 : screen.blit(tetris_5,((xline*one_pixel_size) + White_space+width,(yline*one_pixel_size) + White_space+height))
                    if next_tile_map[yline][xline] == 6 : screen.blit(tetris_6,((xline*one_pixel_size) + White_space+width,(yline*one_pixel_size) + White_space+height))
                    if next_tile_map[yline][xline] == 7 : screen.blit(tetris_7,((xline*one_pixel_size) + White_space+width,(yline*one_pixel_size) + White_space+height))

def view_next_shape_clear():
    for num in range(3):
        if len(next_tile_map) == num + 2 : 
            if num + 2 == 4 : width, height = 376, 56
            if num + 2 == 3 : width, height = 390, 70
            if num + 2 == 2 : width, height = 405, 83
            for yline in range(num + 2):
                for xline in range(num + 2):
                    pygame.draw.rect(screen,[0,0,0], (((one_pixel_size * xline) + White_space)+width, (one_pixel_size * yline) + White_space+height, one_pixel_size - 2,one_pixel_size - 2))

def view_pygame_map():
    for yline in range(yline_num):
        for xline in range(xline_num):
            if tile_map[yline][xline] == 0 :
                pygame.draw.rect(screen,[0,0,0], ((one_pixel_size * xline) + White_space, (one_pixel_size * yline) + White_space, one_pixel_size - 2,one_pixel_size - 2))
            if move_map[yline][xline] == 1 : screen.blit(tetris_1,((xline*one_pixel_size) + White_space,(yline*one_pixel_size) + White_space))
            if move_map[yline][xline] == 2 : screen.blit(tetris_2,((xline*one_pixel_size) + White_space,(yline*one_pixel_size) + White_space))
            if move_map[yline][xline] == 3 : screen.blit(tetris_3,((xline*one_pixel_size) + White_space,(yline*one_pixel_size) + White_space))
            if move_map[yline][xline] == 4 : screen.blit(tetris_4,((xline*one_pixel_size) + White_space,(yline*one_pixel_size) + White_space))
            if move_map[yline][xline] == 5 : screen.blit(tetris_5,((xline*one_pixel_size) + White_space,(yline*one_pixel_size) + White_space))
            if move_map[yline][xline] == 6 : screen.blit(tetris_6,((xline*one_pixel_size) + White_space,(yline*one_pixel_size) + White_space))
            if move_map[yline][xline] == 7 : screen.blit(tetris_7,((xline*one_pixel_size) + White_space,(yline*one_pixel_size) + White_space))
            if tile_map[yline][xline] == 9 : screen.blit(tetris_9,((xline*one_pixel_size) + White_space,(yline*one_pixel_size) + White_space))
            if tile_map[yline][xline] == 1 :
                pygame.draw.rect(screen,[100,100,100], ((one_pixel_size * xline) + White_space, (one_pixel_size * yline) + White_space, one_pixel_size - 2,one_pixel_size - 2))

def test_1Sec():
    global test_count40
    test_count40 += 1
    print(f"{test_count40}")
    if test_count40 == time_count: test_count40 = 0
    return test_count40
schedule.every(10).seconds.do(test_1Sec)

def select_figure():
    global now_result, now_result2, move_figure, next_result, next_result2
    if next_result != 9:
        now_result = next_result
        now_result2 = next_result2
    next_result = random.choice(figure_num)
    if len(figure_shape[now_result][1][1]) == 4 :
        next_result2 = random.choice(figure_num_direction1)
    if len(figure_shape[now_result][1][1]) == 3 :
        next_result2 = random.choice(figure_num_direction2)
    if len(figure_shape[now_result][1][1]) == 2 :
        next_result2 = random.choice(figure_num_direction3)
    move_figure = 1

def down_figure():
    global y_line_down, x_line_side, time_count, experience
    try :
        if len(figure_shape[now_result][1][1]) == 4 :
            if y_line_down >= 0 :
                move_map[y_line_down  ][x_line_side+(0)] = figure_shape[now_result][now_result2][3][0]
                move_map[y_line_down  ][x_line_side+(1)] = figure_shape[now_result][now_result2][3][1]
                move_map[y_line_down  ][x_line_side+(2)] = figure_shape[now_result][now_result2][3][2]
                move_map[y_line_down  ][x_line_side+(3)] = figure_shape[now_result][now_result2][3][3]
            if y_line_down >= 1 :
                move_map[y_line_down-1][x_line_side+(0)] = figure_shape[now_result][now_result2][2][0]
                move_map[y_line_down-1][x_line_side+(1)] = figure_shape[now_result][now_result2][2][1]
                move_map[y_line_down-1][x_line_side+(2)] = figure_shape[now_result][now_result2][2][2]
                move_map[y_line_down-1][x_line_side+(3)] = figure_shape[now_result][now_result2][2][3]
            if y_line_down >= 2 :
                move_map[y_line_down-2][x_line_side+(0)] = figure_shape[now_result][now_result2][1][0]
                move_map[y_line_down-2][x_line_side+(1)] = figure_shape[now_result][now_result2][1][1]
                move_map[y_line_down-2][x_line_side+(2)] = figure_shape[now_result][now_result2][1][2]
                move_map[y_line_down-2][x_line_side+(3)] = figure_shape[now_result][now_result2][1][3]
            if y_line_down >= 3 :
                move_map[y_line_down-3][x_line_side+(0)] = figure_shape[now_result][now_result2][0][0]
                move_map[y_line_down-3][x_line_side+(1)] = figure_shape[now_result][now_result2][0][1]
                move_map[y_line_down-3][x_line_side+(2)] = figure_shape[now_result][now_result2][0][2]
                move_map[y_line_down-3][x_line_side+(3)] = figure_shape[now_result][now_result2][0][3]
            if y_line_down >= 4 :
                move_map[y_line_down-4][x_line_side+(0)] = 0
                move_map[y_line_down-4][x_line_side+(1)] = 0
                move_map[y_line_down-4][x_line_side+(2)] = 0
                move_map[y_line_down-4][x_line_side+(3)] = 0
        if len(figure_shape[now_result][1][1]) == 3 :
            if y_line_down >= 0 :
                move_map[y_line_down  ][x_line_side+( 0)] = figure_shape[now_result][now_result2][2][0]
                move_map[y_line_down  ][x_line_side+( 1)] = figure_shape[now_result][now_result2][2][1]
                move_map[y_line_down  ][x_line_side+( 2)] = figure_shape[now_result][now_result2][2][2]
            if y_line_down >= 1 :
                move_map[y_line_down-1][x_line_side+( 0)] = figure_shape[now_result][now_result2][1][0]
                move_map[y_line_down-1][x_line_side+( 1)] = figure_shape[now_result][now_result2][1][1]
                move_map[y_line_down-1][x_line_side+( 2)] = figure_shape[now_result][now_result2][1][2]
            if y_line_down >= 2 :
                move_map[y_line_down-2][x_line_side+( 0)] = figure_shape[now_result][now_result2][0][0]
                move_map[y_line_down-2][x_line_side+( 1)] = figure_shape[now_result][now_result2][0][1]
                move_map[y_line_down-2][x_line_side+( 2)] = figure_shape[now_result][now_result2][0][2]
            if y_line_down >= 3 :
                move_map[y_line_down-3][x_line_side+( 0)] = 0
                move_map[y_line_down-3][x_line_side+( 1)] = 0
                move_map[y_line_down-3][x_line_side+( 2)] = 0
        if len(figure_shape[now_result][1][1]) == 2 :
            if y_line_down >= 0 :
                move_map[y_line_down  ][x_line_side+( 0)] = figure_shape[now_result][now_result2][1][0]
                move_map[y_line_down  ][x_line_side+( 1)] = figure_shape[now_result][now_result2][1][1]
            if y_line_down >= 1 :
                move_map[y_line_down-1][x_line_side+( 0)] = figure_shape[now_result][now_result2][0][0]
                move_map[y_line_down-1][x_line_side+( 1)] = figure_shape[now_result][now_result2][0][1]
            if y_line_down >= 2 :
                move_map[y_line_down-2][x_line_side+( 0)] = 0
                move_map[y_line_down-2][x_line_side+( 1)] = 0
    except IndexError: ''           

    if test_count40 == time_count-1 : y_line_down = y_line_down + 1
    if time_count == 43 - (level * 3) : experience = experience + 1
    if test_count40 == 0:
        os.system("cls")
        view_terminal_map()
        view_terminal_inf()
    level_up()
    down_end()

def view_terminal_inf():
    print("경험치 : ",experience)
    print("레벨 : ",level)
    print("점수 : ",score)
    print("라인삭제 : ",lines)

def up_click():
    global now_result2, x_line_side
    if now_result2 != 4 : now_result2 = now_result2 + 1
    if now_result2 == 4 : now_result2 = 0
    down_figure()
    for y2 in range(1,21): 
        if move_map[y2][10] != 0 : left_click()
    for y1 in range(1,21):
        if move_map[y1][1]  != 0 : right_click()
    os.system("cls")
    # view_terminal_map()

def down_click():
    global test_count40
    test_count40 = time_count-1

def right_click():
    try :
        global x_line_side, move_close_right
        for y2 in range(22): 
            if len(figure_shape[now_result][1][1]) == 4 : move_map[y2][x_line_side] = 0
            if len(figure_shape[now_result][1][1]) == 3 : move_map[y2][x_line_side] = 0
            if len(figure_shape[now_result][1][1]) == 2 : move_map[y2][x_line_side] = 0
        if len(figure_shape[now_result][1][1]) >= 4 : 
            if   move_map[y_line_down-3][x_line_side+2] >= 1 and  tile_map[y_line_down-3][x_line_side+3] == 1: move_close_right = 1
            if   move_map[y_line_down-3][x_line_side+3] >= 1 and  tile_map[y_line_down-3][x_line_side+4] == 1: move_close_right = 1
            if   move_map[y_line_down  ][x_line_side+3] >= 1 and  tile_map[y_line_down  ][x_line_side+4] == 1: move_close_right = 1
            if   move_map[y_line_down-1][x_line_side+3] >= 1 and  tile_map[y_line_down-1][x_line_side+4] == 1: move_close_right = 1
            if   move_map[y_line_down-2][x_line_side+3] >= 1 and  tile_map[y_line_down-2][x_line_side+4] == 1: move_close_right = 1
        if len(figure_shape[now_result][1][1]) >= 3 : 
            if   move_map[y_line_down-2][x_line_side+1] >= 1 and  tile_map[y_line_down-2][x_line_side+2] == 1: move_close_right = 1
            if   move_map[y_line_down-2][x_line_side+2] >= 1 and  tile_map[y_line_down-2][x_line_side+3] == 1: move_close_right = 1
            if   move_map[y_line_down  ][x_line_side+2] >= 1 and  tile_map[y_line_down  ][x_line_side+3] == 1: move_close_right = 1
            if   move_map[y_line_down-1][x_line_side+2] >= 1 and  tile_map[y_line_down-1][x_line_side+3] == 1: move_close_right = 1
        if len(figure_shape[now_result][1][1]) >= 2 : 
            if   move_map[y_line_down  ][x_line_side  ] >= 1 and  tile_map[y_line_down  ][x_line_side+1] == 1: move_close_right = 1
            if   move_map[y_line_down-1][x_line_side  ] >= 1 and  tile_map[y_line_down-1][x_line_side+1] == 1: move_close_right = 1
            if   move_map[y_line_down  ][x_line_side+1] >= 1 and  tile_map[y_line_down  ][x_line_side+2] == 1: move_close_right = 1
            if   move_map[y_line_down-1][x_line_side+1] >= 1 and  tile_map[y_line_down-1][x_line_side+2] == 1: move_close_right = 1
        for y2 in range(1,21): 
            if move_map[y2][10] != 0 : move_close_right = 1
        if move_close_right     != 1 : x_line_side = x_line_side + 1
    except IndexError: ''        
    
def left_click():
    try :
        global x_line_side, move_close_left, x_line_side
        for y1 in range(22):
            if len(figure_shape[now_result][1][1]) == 4 : move_map[y1][x_line_side+3] = 0
            if len(figure_shape[now_result][1][1]) == 3 : move_map[y1][x_line_side+2] = 0
            if len(figure_shape[now_result][1][1]) == 2 : move_map[y1][x_line_side+1] = 0
        if len(figure_shape[now_result][1][1]) >= 4 : 
            if   move_map[y_line_down-3][x_line_side  ] >= 1 and  tile_map[y_line_down-3][x_line_side-1] == 1: move_close_left = 1
            if   move_map[y_line_down-3][x_line_side+1] >= 1 and  tile_map[y_line_down-3][x_line_side  ] == 1: move_close_left = 1
        if len(figure_shape[now_result][1][1]) >= 3 : 
            if   move_map[y_line_down-2][x_line_side  ] >= 1 and  tile_map[y_line_down-2][x_line_side-1] == 1: move_close_left = 1
            if   move_map[y_line_down-2][x_line_side+1] >= 1 and  tile_map[y_line_down-2][x_line_side  ] == 1: move_close_left = 1
        if len(figure_shape[now_result][1][1]) >= 2 : 
            if   move_map[y_line_down  ][x_line_side  ] >= 1 and  tile_map[y_line_down  ][x_line_side-1] == 1: move_close_left = 1
            if   move_map[y_line_down  ][x_line_side+1] >= 1 and  tile_map[y_line_down  ][x_line_side  ] == 1: move_close_left = 1
            if   move_map[y_line_down-1][x_line_side  ] >= 1 and  tile_map[y_line_down-1][x_line_side-1] == 1: move_close_left = 1
            if   move_map[y_line_down-1][x_line_side+1] >= 1 and  tile_map[y_line_down-1][x_line_side  ] == 1: move_close_left = 1
        for y1 in range(1,21):
            if move_map[y1][1] != 0 : move_close_left = 1
        if move_close_left     != 1 : x_line_side = x_line_side - 1
    except IndexError: ''        

def down_end():
    if len(figure_shape[now_result][1][1]) == 4 :
        if y_line_down < 21 and y_line_down > 1:
            if   move_map[y_line_down  ][x_line_side+(0)] >= 1 and tile_map[y_line_down+1][x_line_side+(0)] >= 1 and x_line_side >  0 : down_stop()
            # if   move_map[y_line_down  ][x_line_side+(1)] >= 1 and tile_map[y_line_down+1][x_line_side+(1)] >= 1 and x_line_side < 10 : down_stop()
            if   move_map[y_line_down  ][x_line_side+(2)] >= 1 and tile_map[y_line_down+1][x_line_side+(2)] >= 1 and x_line_side <  9 : down_stop()
            if   move_map[y_line_down  ][x_line_side+(3)] >= 1 and tile_map[y_line_down+1][x_line_side+(3)] >= 1 and x_line_side <  8 : down_stop()
            if   move_map[y_line_down-1][x_line_side+(0)] >= 1 and tile_map[y_line_down  ][x_line_side+(0)] >= 1 and x_line_side >  0 : down_stop()
            if   move_map[y_line_down-1][x_line_side+(1)] >= 1 and tile_map[y_line_down  ][x_line_side+(1)] >= 1 and x_line_side < 10 : down_stop()
            if   move_map[y_line_down-1][x_line_side+(2)] >= 1 and tile_map[y_line_down  ][x_line_side+(2)] >= 1 and x_line_side <  9 : down_stop()
            if   move_map[y_line_down-1][x_line_side+(3)] >= 1 and tile_map[y_line_down  ][x_line_side+(3)] >= 1 and x_line_side <  8 : down_stop()
            if   move_map[y_line_down-2][x_line_side+(0)] >= 1 and tile_map[y_line_down-1][x_line_side+(0)] >= 1 and x_line_side >  0 : down_stop()
            if   move_map[y_line_down-2][x_line_side+(1)] >= 1 and tile_map[y_line_down-1][x_line_side+(1)] >= 1 and x_line_side < 10 : down_stop()
            if   move_map[y_line_down-2][x_line_side+(2)] >= 1 and tile_map[y_line_down-1][x_line_side+(2)] >= 1 and x_line_side <  9 : down_stop()
            if   move_map[y_line_down-2][x_line_side+(3)] >= 1 and tile_map[y_line_down-1][x_line_side+(3)] >= 1 and x_line_side <  8 : down_stop()
        elif y_line_down == 21 and (now_result2 == 0 or now_result2 == 2) : down_stop()
        elif y_line_down == 22 and (now_result2 == 1 or now_result2 == 3) : down_stop()
    if len(figure_shape[now_result][1][1]) == 3 :
        if y_line_down < 21 and y_line_down > 1:  
            if   move_map[y_line_down  ][x_line_side+(0)] >= 1 and tile_map[y_line_down+1][x_line_side+(0)] >= 1 and x_line_side != 0   : down_stop()
            if   move_map[y_line_down  ][x_line_side+(1)] >= 1 and tile_map[y_line_down+1][x_line_side+(1)] >= 1 and x_line_side != 10  : down_stop()
            if   move_map[y_line_down  ][x_line_side+(2)] >= 1 and tile_map[y_line_down+1][x_line_side+(2)] >= 1 and x_line_side != 9   : down_stop()
            if   move_map[y_line_down-1][x_line_side+(0)] >= 1 and tile_map[y_line_down  ][x_line_side+(0)] >= 1 and x_line_side != 0   : down_stop()
            if   move_map[y_line_down-1][x_line_side+(1)] >= 1 and tile_map[y_line_down  ][x_line_side+(1)] >= 1 and x_line_side != 10  : down_stop()
            if   move_map[y_line_down-1][x_line_side+(2)] >= 1 and tile_map[y_line_down  ][x_line_side+(2)] >= 1 and x_line_side != 9   : down_stop()
            if   move_map[y_line_down-2][x_line_side+(0)] >= 1 and tile_map[y_line_down-1][x_line_side+(0)] >= 1 and x_line_side != 0   : down_stop()
            if   move_map[y_line_down-2][x_line_side+(1)] >= 1 and tile_map[y_line_down-1][x_line_side+(1)] >= 1 and x_line_side != 10  : down_stop()
            if   move_map[y_line_down-2][x_line_side+(2)] >= 1 and tile_map[y_line_down-1][x_line_side+(2)] >= 1 and x_line_side != 9   : down_stop()
        if y_line_down == 21 :
            if ((now_result == 1 and now_result2 == 3) or (now_result == 2 and now_result2 == 1) or (now_result == 5 and now_result2 == 0)) : ''
            else : down_stop()
        if y_line_down == 22 : down_stop()
    if len(figure_shape[now_result][1][1]) == 2 :
        if   y_line_down < 21  :
            if   move_map[y_line_down  ][x_line_side+(0)] >= 1 and tile_map[y_line_down+1][x_line_side+(0)] >= 1: down_stop()
            if   move_map[y_line_down  ][x_line_side+(1)] >= 1 and tile_map[y_line_down+1][x_line_side+(1)] >= 1: down_stop()
            if   move_map[y_line_down-1][x_line_side+(0)] >= 1 and tile_map[y_line_down  ][x_line_side+(0)] >= 1: down_stop()
            if   move_map[y_line_down-1][x_line_side+(1)] >= 1 and tile_map[y_line_down  ][x_line_side+(1)] >= 1: down_stop()
        elif y_line_down == 21 : down_stop()      
            
def down_stop():
    global move_figure, y_line_down, x_line_side
    for yline in range(22):
        for xline in range(12):
            if tile_map[yline][xline] == 0 and move_map[yline][xline] >= 1: tile_map[yline][xline] = 1
            if tile_map[yline][xline] == 1 and yline == 1:
                restart()
    clear_map()
    move_figure = 0
    y_line_down = 1
    x_line_side = 4
    make_move_map()

def spacebal_click():
    global y_line_down, test_count40, time_count
    while True :
        if y_line_down == 1:
            break
        down_figure()
        test_count40 = time_count-1

def level_up():
    global level, experience, time_count
    if experience <  1000 : level = 1
    if experience >= 1000  and experience < 2500  : level = 2
    if experience >= 2500  and experience < 4000  : level = 3
    if experience >= 4000  and experience < 5500  : level = 4
    if experience >= 5500  and experience < 7000  : level = 5
    if experience >= 7000  and experience < 8500  : level = 6
    if experience >= 8500  and experience < 10000 : level = 7
    if experience >= 10000 and experience < 11500 : level = 8
    if experience >= 11500 and experience < 13000 : level = 9
    if experience >= 13000 and experience < 14500 : level = 10
    if experience >= 14500 and experience < 16000 : level = 11
    if experience >= 16000 : level = 12
    time_count = 43 - (level * 3)

def clear_map():
    global lines, score, experience
    once_clear_line = 0
    for line in range(1,21):
        if tile_map[line] == [9,1,1,1,1,1,1,1,1,1,1,9]:
            del tile_map[line]
            tile_map.insert(1,[9,0,0,0,0,0,0,0,0,0,0,9])
            lines = lines + 1
            once_clear_line = once_clear_line + 1
            experience = experience + 100
    if once_clear_line == 1 : score = score + 10
    if once_clear_line == 2 : score = score + 30
    if once_clear_line == 3 : score = score + 60
    if once_clear_line == 4 : score = score + 100
    level_up()
            
def run_first():
    global background_num, y_line_down, x_line_side, now_result, now_result2
    if test_count40 == time_count-1: background_num = background_num + 1
    if background_num != 2 :
        screen.blit(background,(0,0))
    if background_num == 2 :
        screen.fill((0,0,0))
        now_result = random.choice(figure_num)
        if len(figure_shape[now_result][1][1]) == 4 :
            now_result2 = random.choice(figure_num_direction1)
        if len(figure_shape[now_result][1][1]) == 3 :
            now_result2 = random.choice(figure_num_direction2)
        if len(figure_shape[now_result][1][1]) == 2 :
            now_result2 = random.choice(figure_num_direction3)
        view_help_message()
def restart():
    first_setting()
    sceond_setting()
    make_tile_map()
    make_move_map()
    
def run_program():
    global move_close_left, move_close_right, selcet, background_num
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 게임 화면 종료
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN: ''
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if (keys[pygame.K_SPACE])  : spacebal_click()
                if (keys[pygame.K_TAB])    : 
                    print("K_TAB 누름")
                    restart()
                if (keys[pygame.K_ESCAPE]) : 
                    print("K_ESCAPE 누름")
                    pygame.quit()
                    sys.exit()
                if (keys[pygame.K_LEFT])   : left_click()
                if (keys[pygame.K_RIGHT])  : right_click()
                if (keys[pygame.K_UP])     : up_click()
                if (keys[pygame.K_DOWN])   : down_click()
        move_close_left = 0
        move_close_right = 0


        if background_num != 2:
            run_first()
        if background_num == 2:
            if move_figure == 0: 
                change_score()
                view_change_score()
                view_next_shape_clear()
                select_figure()
                view_next_shape()
            if move_figure == 1: 
                down_figure()
            view_pygame_map()

        test_1Sec()
        clock.tick(30)
        schedule.run_pending()
        pygame.display.update()
        
run_program()



