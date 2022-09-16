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
    
    global yline_num, xline_num, one_pixel_size, White_space
    xline_num = 10          ## X라인 개수
    yline_num = 20          ## Y라인 개수
    White_space = 5
    one_pixel_size = 30

    global tile_map, move_map, test_count5, time_count, done, screen, clock, y_line_down, move_figure, x_line_side, move_close_left, move_close_right
    size = [(xline_num*one_pixel_size)+(White_space*2), (yline_num*one_pixel_size)+(White_space*2)]
    done = False
    screen = pygame.display.set_mode(size)
    screen.fill([255,255,255])
    clock = pygame.time.Clock()
    test_count5 = 0
    tile_map = []
    move_map = []
    time_count = 40
    y_line_down = 0
    x_line_side = 0
    move_figure = 0
    move_close_left = 0
    move_close_right = 0

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
                    
        [[[0,1,0], 
         [0,1,0], 
         [0,1,1]],
        [[0,0,0],   
         [1,1,1], 
         [1,0,0]],
        [[1,1,0],   
         [0,1,0], 
         [0,1,0]],
        [[0,0,1],   
         [1,1,1], 
         [0,0,0]]],
        
        [[[0,1,0], 
         [0,1,0], 
         [1,1,0]],
        [[1,0,0],   
         [1,1,1], 
         [0,0,0]],
        [[0,1,1],   
         [0,1,0], 
         [0,1,0]],
        [[0,0,0],   
         [1,1,1], 
         [0,0,1]]],
        
        [[[0,0,0], 
         [0,1,1], 
         [1,1,0]],
        [[0,1,0],   
         [0,1,1], 
         [0,0,1]],
        [[0,0,0],   
         [0,1,1], 
         [1,1,0]],
        [[0,1,0],   
         [0,1,1], 
         [0,0,1]]],
        
        [[[0,0,0], 
         [1,1,0], 
         [0,1,1]],
        [[0,1,0],   
         [1,1,0], 
         [1,0,0]],
        [[0,0,0],   
         [1,1,0], 
         [0,1,1]],
        [[0,1,0],   
         [1,1,0], 
         [1,0,0]]],
        
        [[[0,1,0], 
         [1,1,1], 
         [0,0,0]],
        [[0,1,0],   
         [0,1,1], 
         [0,1,0]],
        [[0,0,0],   
         [1,1,1], 
         [0,1,0]],
        [[0,1,0],   
         [1,1,0], 
         [0,1,0]]],
        
        [[[1,1], 
         [1,1]],
        [[1,1], 
         [1,1]],
        [[1,1], 
         [1,1]],
        [[1,1], 
         [1,1]]]]

    global background, tetris_1, tetris_2, tetris_3, tetris_4 , tetris_5 , tetris_6 , tetris_7        # 기초 배치 이미지
    background = pygame.transform.scale(pygame.image.load('image/tetris_start_background.jpg'), (50, 50))
    tetris_1 = pygame.transform.scale(pygame.image.load('image/teteris_1.png'), (30, 30))
    tetris_2 = pygame.transform.scale(pygame.image.load('image/teteris_2.png'), (30, 30))
    tetris_3 = pygame.transform.scale(pygame.image.load('image/teteris_3.png'), (30, 30))
    tetris_4 = pygame.transform.scale(pygame.image.load('image/teteris_4.png'), (30, 30))
    tetris_5 = pygame.transform.scale(pygame.image.load('image/teteris_5.png'), (30, 30))
    tetris_6 = pygame.transform.scale(pygame.image.load('image/teteris_6.png'), (30, 30))
    tetris_7 = pygame.transform.scale(pygame.image.load('image/teteris_7.png'), (30, 30))
first_setting()

def make_tile_map():
    tile_map.clear()
    for yline in range(yline_num):
        etc_map = []
        for xline in range(xline_num):
            etc_map.append(0)
        tile_map.append(0)
        tile_map[yline] = etc_map
make_tile_map()

def make_move_map():
    move_map.clear()
    for yline in range(yline_num):
        etc2_map = []
        for xline in range(xline_num):
            etc2_map.append(0)
        move_map.append(0)
        move_map[yline] = etc2_map
make_move_map()

def tile_map_move_map():
    for yline in range(yline_num):
        for xline in range(xline_num):
            if tile_map[yline][xline] == 0 and move_map[yline][xline] == 1:
                tile_map[yline][xline] = 1

def display_terminal_map():
    for yline in range(yline_num):
        for xline in range(xline_num):
            print(tile_map[yline][xline], end=' ')
        print()
display_terminal_map()

def view_pygame_map():
    for yline in range(yline_num):
        for xline in range(xline_num):
            if tile_map[yline][xline] == 0 :
                pygame.draw.rect(screen,[0,0,0],       ((one_pixel_size * xline) + White_space, (one_pixel_size * yline) + White_space, one_pixel_size - 2,one_pixel_size - 2))
            if tile_map[yline][xline] == 1 :
                pygame.draw.rect(screen,[100,100,100], ((one_pixel_size * xline) + White_space, (one_pixel_size * yline) + White_space, one_pixel_size - 2,one_pixel_size - 2))
            if move_map[yline][xline] == 1 :
                pygame.draw.rect(screen,[100,100,100], ((one_pixel_size * xline) + White_space, (one_pixel_size * yline) + White_space, one_pixel_size - 2,one_pixel_size - 2))

def test_1Sec():
    global test_count5
    test_count5 += 1
    # print(f"{test_count5}")
    if test_count5 == time_count:
        test_count5 = 0
    return test_count5
schedule.every(10).seconds.do(test_1Sec)

def select_figure():
    global result, result2, move_figure
    result = random.choice(figure_num)
    # result = 0
    if len(figure_shape[result][1][1]) == 4 :
        result2 = random.choice(figure_num_direction1)
    if len(figure_shape[result][1][1]) == 3 :
        result2 = random.choice(figure_num_direction2)
    if len(figure_shape[result][1][1]) == 2 :
        result2 = random.choice(figure_num_direction3)
    move_figure = 1

def down_figure():
    global y_line_down, x_line_side, time_count
    try :
        if len(figure_shape[result][1][1]) == 4 :
            if y_line_down >= 0 :
                move_map[y_line_down  ][x_line_side+(0)] = figure_shape[result][result2][3][0]
                move_map[y_line_down  ][x_line_side+(1)] = figure_shape[result][result2][3][1]
                move_map[y_line_down  ][x_line_side+(2)] = figure_shape[result][result2][3][2]
                move_map[y_line_down  ][x_line_side+(3)] = figure_shape[result][result2][3][3]
            if y_line_down >= 1 :
                move_map[y_line_down-1][x_line_side+(0)] = figure_shape[result][result2][2][0]
                move_map[y_line_down-1][x_line_side+(1)] = figure_shape[result][result2][2][1]
                move_map[y_line_down-1][x_line_side+(2)] = figure_shape[result][result2][2][2]
                move_map[y_line_down-1][x_line_side+(3)] = figure_shape[result][result2][2][3]
            if y_line_down >= 2 :
                move_map[y_line_down-2][x_line_side+(0)] = figure_shape[result][result2][1][0]
                move_map[y_line_down-2][x_line_side+(1)] = figure_shape[result][result2][1][1]
                move_map[y_line_down-2][x_line_side+(2)] = figure_shape[result][result2][1][2]
                move_map[y_line_down-2][x_line_side+(3)] = figure_shape[result][result2][1][3]
            if y_line_down >= 3 :
                move_map[y_line_down-3][x_line_side+(0)] = figure_shape[result][result2][0][0]
                move_map[y_line_down-3][x_line_side+(1)] = figure_shape[result][result2][0][1]
                move_map[y_line_down-3][x_line_side+(2)] = figure_shape[result][result2][0][2]
                move_map[y_line_down-3][x_line_side+(3)] = figure_shape[result][result2][0][3]
            if y_line_down >= 4 :
                move_map[y_line_down-4][x_line_side+(0)] = 0
                move_map[y_line_down-4][x_line_side+(1)] = 0
                move_map[y_line_down-4][x_line_side+(2)] = 0
                move_map[y_line_down-4][x_line_side+(3)] = 0
        if len(figure_shape[result][1][1]) == 3 :
            if y_line_down >= 0 :
                move_map[y_line_down  ][x_line_side+( 0)] = figure_shape[result][result2][2][0]
                move_map[y_line_down  ][x_line_side+( 1)] = figure_shape[result][result2][2][1]
                move_map[y_line_down  ][x_line_side+( 2)] = figure_shape[result][result2][2][2]
            if y_line_down >= 1 :
                move_map[y_line_down-1][x_line_side+( 0)] = figure_shape[result][result2][1][0]
                move_map[y_line_down-1][x_line_side+( 1)] = figure_shape[result][result2][1][1]
                move_map[y_line_down-1][x_line_side+( 2)] = figure_shape[result][result2][1][2]
            if y_line_down >= 2 :
                move_map[y_line_down-2][x_line_side+( 0)] = figure_shape[result][result2][0][0]
                move_map[y_line_down-2][x_line_side+( 1)] = figure_shape[result][result2][0][1]
                move_map[y_line_down-2][x_line_side+( 2)] = figure_shape[result][result2][0][2]
            if y_line_down >= 3 :
                move_map[y_line_down-3][x_line_side+( 0)] = 0
                move_map[y_line_down-3][x_line_side+( 1)] = 0
                move_map[y_line_down-3][x_line_side+( 2)] = 0
        if len(figure_shape[result][1][1]) == 2 :
            if y_line_down >= 0 :
                move_map[y_line_down  ][x_line_side+( 0)] = figure_shape[result][result2][1][0]
                move_map[y_line_down  ][x_line_side+( 1)] = figure_shape[result][result2][1][1]
            if y_line_down >= 1 :
                move_map[y_line_down-1][x_line_side+( 0)] = figure_shape[result][result2][0][0]
                move_map[y_line_down-1][x_line_side+( 1)] = figure_shape[result][result2][0][1]
            if y_line_down >= 2 :
                move_map[y_line_down-2][x_line_side+( 0)] = 0
                move_map[y_line_down-2][x_line_side+( 1)] = 0
    except IndexError:
        ''           
    if len(figure_shape[result][1][1]) == 4 :         
        if (y_line_down == 19 and (move_map[y_line_down  ][x_line_side+( 0)] == 1 or move_map[y_line_down][x_line_side+( 1)] == 1 or move_map[y_line_down][x_line_side+( 2)] == 1 or move_map[y_line_down][x_line_side+( 3)] == 1)):
            for n in range(20):
                for m in range(10):
                    tile_map_move_map()
                    y_line_down = 0
                    x_line_side = 0
                    select_figure()
    if test_count5 == time_count-1 :
        y_line_down = y_line_down + 1
        os.system("cls")
        display_terminal_map()
    

def figure_move_rule():
    global x_line_side, move_close_left, move_close_right
    for y in range(20):
        if move_map[y][0] == 1 and move_map[y][9] == 1:
            move_map[y][9] = 0
            move_map[y-1][9] = 0
            move_map[y+1][9] = 0
        right_move()
            
        # if move_map[y][0] == 1 and move_map[y][1] == 1 and move_map[y][9] == 1 and move_map[y][8] == 1:
        #     move_map[y][9] = 0
        #     move_map[y-1][9] = 0
        #     move_map[y+1][9] = 0
        #     move_map[y][8] = 0
        #     move_map[y-1][8] = 0
        #     move_map[y+1][8] = 0
        #     x_line_side = x_line_side + 2
            
def right_move():
    global x_line_side, move_close_right
    for y2 in range(20): 
        if move_map[y2][9] == 1:
            move_close_right = 1
        if len(figure_shape[result][1][1]) == 4 : 
            move_map[y2][x_line_side] = 0
        if len(figure_shape[result][1][1]) == 3 : 
            move_map[y2][x_line_side] = 0
        if len(figure_shape[result][1][1]) == 2 : 
            move_map[y2][x_line_side] = 0
    if move_close_right  != 1 : 
        x_line_side = x_line_side + 1
    
def left_move():
    global x_line_side, move_close_left
    for y1 in range(20):
        if move_map[y1][0] == 1:
            move_close_left = 1
        if len(figure_shape[result][1][1]) == 4 : 
            move_map[y1][x_line_side+3] = 0
        if len(figure_shape[result][1][1]) == 3 : 
            move_map[y1][x_line_side+2] = 0
        if len(figure_shape[result][1][1]) == 2 : 
            move_map[y1][x_line_side+1] = 0
    if move_close_left != 1 : 
        x_line_side = x_line_side - 1
        
def run_program():
    global x_line_side, y_line_down, result2, move_close_left, move_close_right, move_figure, test_count5
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 게임 화면 종료
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                ''
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                
                if (keys[pygame.K_SPACE]):
                    print("K_SPACE 누름")
                    make_tile_map()
                    select_figure()
                if (keys[pygame.K_TAB]): 
                    print("K_TAB 누름")
                if (keys[pygame.K_ESCAPE]):
                    print("K_ESCAPE 누름")
                    pygame.quit()
                    sys.exit()
                if (keys[pygame.K_LEFT]):
                    left_move()
                if (keys[pygame.K_RIGHT]):
                    right_move()
                if (keys[pygame.K_UP]):
                    if result2 != 4 :
                        result2 = result2 + 1
                    if result2 == 4 :
                        result2 = 0
                if (keys[pygame.K_DOWN]):
                    test_count5 = time_count-1
                    view_pygame_map()
                    
        move_close_left = 0
        move_close_right = 0
        view_pygame_map()
        if move_figure == 0:
            select_figure()
        if move_figure == 1:
            down_figure()

                    
                    
        test_1Sec()
        clock.tick(30)
        schedule.run_pending()
        pygame.display.update()
        
run_program()