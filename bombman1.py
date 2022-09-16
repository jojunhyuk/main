import os
from re import A, I
import pygame
import sys
import math
import schedule
import random
from datetime import datetime
from pygame.locals import *

# pyinstaller -w -F onecard.py
os.system("cls")
pygame.init()

dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir)

######################################################### 

######################################################### 기본 맵, 나열 맵, x축, y축 출력 map_open()
def map_open():
    map_txt = open('./txt/maze_py.txt', 'r', encoding='utf-8')
    global x_line, y_line, trans_map, origin_map
    origin_map = map_txt.read()
    x_line = origin_map.replace(' ','').find('\n')
    y_line = int(len(origin_map.replace(' ','').replace('\n',''))/x_line)
    trans_map = origin_map.replace(' ','').replace('\n','')
    map_txt.close()
map_open()
######################################################### 기초 배열 맵 출력 map_clear()
# use_map = []
tile_map = []
def map_clear():
    tile_map.clear()
    map_txt = open('./txt/maze_py.txt', 'r', encoding='utf-8')
    while True:
        line_map = map_txt.readline()
        if not line_map:
            break
        line_map = line_map.replace('\n','')
        clear_map = line_map.split(' ')
        tile_map.append(clear_map)
        # use_map.append(clear_map)
    map_txt.close()
map_clear()
######################################################### 폭탄 배열 맵 출력
def map_bomb():
    global bomb_map
    bomb_map = [[0]*y_line for _ in range(y_line)]

    for a in range(y_line):
        for b in range(x_line):
            bomb_map[a][b] = tile_map[a][b]
        

    for a in range(y_line):
        for b in range(x_line):
            bomb_map[a][b] = 'o'
map_bomb()
######################################################### 파이게임 정보 입력
def setting():

    size = [x_line*50, y_line*50]

    global player_x_pos, player_y_pos, count
    player_x_pos = 50
    player_y_pos = 50
    count = 0
    
    global bomb_list, bomb_count, bomb_click, bomb_num, bomb_limit
    bomb_list = []
    bomb_count = [0,0,0]
    bomb_click = 0
    bomb_num = 0
    
    bomb_limit = 2
    bomb_power = 0
    
    
    global screen, done, clock, test_count5, restart, restart_count, ghost_num, ghost_list, ghost_total, move_count50, move_total_result, monster_death
    screen = pygame.display.set_mode(size)
    done = False
    clock = pygame.time.Clock()
    test_count5=0
    restart = 0
    restart_count = 0
    ghost_num = 0
    ghost_list = []
    ghost_total = 0
    move_count50 = 0
    move_total_result = []
    monster_death = 0

    global rock_image, grass_image, bomb_image, boom_image, box_image
    rock_image = pygame.transform.scale(pygame.image.load('image/rock_image.png'), (50, 50))
    grass_image = pygame.transform.scale(pygame.image.load('image/grass_image.png'), (50, 50))
    box_image = pygame.transform.scale(pygame.image.load('image/box_image.png'), (50, 50))
    bomb_image = pygame.transform.scale(pygame.image.load('image/bomb_image.png'), (50, 50))
    boom_image = pygame.transform.scale(pygame.image.load('image/boom.gif'), (50, 50))

    global bombman_down,bombman_up ,bombman_left,bombman_right
    bombman_down = pygame.transform.scale(pygame.image.load('image/bombman_down.png'), (50, 50))
    bombman_up = pygame.transform.scale(pygame.image.load('image/bombman_up.png'), (50, 50))
    bombman_left = pygame.transform.scale(pygame.image.load('image/bombman_left.png'), (50, 50))
    bombman_right = pygame.transform.scale(pygame.image.load('image/bombman_right.png'), (50, 50))
    
    
    global ghost_down,ghost_up ,ghost_left,ghost_right, ghost_face, lose
    ghost_down = pygame.transform.scale(pygame.image.load('image/ghost_down.png'), (50, 50))
    ghost_up = pygame.transform.scale(pygame.image.load('image/ghost_up.png'), (50, 50))
    ghost_left = pygame.transform.scale(pygame.image.load('image/ghost_left.png'), (50, 50))
    ghost_right = pygame.transform.scale(pygame.image.load('image/ghost_right.png'), (50, 50))
    
    global bombman, lose, ghost_face
    bombman = bombman_down
    ghost_face = ghost_down
    lose = pygame.transform.scale(pygame.image.load('image/lose.jpg'), (x_line*50, y_line*50))
setting()

#########################################################         
def display_map():

    global rock_image ,grass_image, bomb_num, restart, count, test_count5
    image_position_x = 0
    image_position_y = 0
    for datas in range(y_line):
        for data in range(x_line):
            if tile_map[datas][data]=='o':
                screen.blit(grass_image,(image_position_x,image_position_y))
            if tile_map[datas][data]=='g':
                screen.blit(grass_image,(image_position_x,image_position_y))
            if tile_map[datas][data]=='p':
                screen.blit(grass_image,(image_position_x,image_position_y))
            if tile_map[datas][data]=='x':
                screen.blit(rock_image,(image_position_x,image_position_y))
            if tile_map[datas][data]=='z':
                screen.blit(grass_image,(image_position_x,image_position_y))
            if tile_map[datas][data]=='b':
                screen.blit(box_image,(image_position_x,image_position_y))
            if tile_map[datas][data]=='t':
                screen.blit(boom_image,(image_position_x,image_position_y))
            if bomb_map[datas][data] == 'p':
                screen.blit(bomb_image,(data*50,datas*50))
                if test_count5 == count + 1:
                    screen.blit(bomb_image,(data*50,datas*50))                   
                if test_count5 == count + 20:
                    if tile_map[datas+1][data] == 'x' :  ''
                    else : 
                        tile_map[datas+1][data] = 't'
                        screen.blit(boom_image,(data*50,datas*50))
                    if tile_map[datas-1][data] == 'x' :  ''
                    else : 
                        tile_map[datas-1][data] = 't'
                        screen.blit(boom_image,(data*50,datas*50))
                    if tile_map[datas][data+1] == 'x' :  ''
                    else : 
                        tile_map[datas][data+1] = 't'
                        screen.blit(boom_image,(data*50,datas*50))
                    if tile_map[datas][data-1] == 'x' :  ''
                    else : 
                        tile_map[datas][data-1] = 't'       
                        screen.blit(boom_image,(data*50,datas*50))   
                    if  tile_map[datas][data] == 'x' :  ''
                    else : 
                        tile_map[datas][data] = 't'       
                                  
                    screen.blit(boom_image,(data*50,datas*50))  
                    if tile_map[player_y_pos//50][player_x_pos//50] == 't': 
                        restart_count = 1
                if test_count5 == count + 21:
                    screen.blit(grass_image,(data*50,datas*50))
                    if tile_map[datas][data] == 't' :
                        tile_map[datas][data] = 'o' 
                    if tile_map[datas][data-1] == 't' :
                        tile_map[datas][data-1] = 'o' 
                    if tile_map[datas][data+1] == 't' :
                        tile_map[datas][data+1] = 'o' 
                    if tile_map[datas-1][data] == 't' :
                        tile_map[datas-1][data] = 'o' 
                    if tile_map[datas+1][data] == 't' :
                        tile_map[datas+1][data] = 'o'   
                    if restart_count == 1: restart = 1
                    map_bomb()
                    bomb_num = bomb_num - 1
            image_position_x += 50
        image_position_y += 50
        image_position_x = 0
    if restart == 1 : 
        lose = pygame.transform.scale(pygame.image.load('image/lose.jpg'), (x_line*50, y_line*50))
        screen.blit(lose,(0,0))
    if restart == 0 : 
        screen.blit(bombman,(player_x_pos,player_y_pos))
######################################################### 
def lose_game():
    if restart == 1 : 
        lose = pygame.transform.scale(pygame.image.load('image/lose.jpg'), (x_line*50, y_line*50))
        screen.blit(lose,(0,0))


######################################################### 시간 카운트 세는 함수(폭탄카운트)
def test_1Sec():
    global test_count5
    test_count5 +=1
    print(f"{test_count5}")
    return test_count5
test_1Sec()
schedule.every(0.1).seconds.do(test_1Sec)
######################################################### 맵에 폭탄 두는 함수
def display_bomb_map():
    global bomb_click, bomb_num, bomb_list, bomb_count, restart, restart_count
    
    if bomb_click == 1 :
        bomb_x = round(player_x_pos/50)
        bomb_y = round(player_y_pos/50)
        if bomb_map[bomb_y][bomb_x] != 'p':
            bomb_num = bomb_num +1
            bomb_map[bomb_y][bomb_x] = 'p'
            bomb_list.append([bomb_x,bomb_y])
            count = test_count5
            if bomb_count[0] == 0 :
                bomb_count[0] = count   
            elif bomb_count[1] == 0 :
                bomb_count[1] = count   
            elif bomb_count[2] == 0 :
                bomb_count[2] = count   
            else :
                ''
            print(test_count5)
            print(bomb_num)
            print(bomb_list)
            print(bomb_count)
        bomb_click = 0 
            
            
            
            
            
            
            
######################################################### 
def ghost_setting():
    global ghost_num, ghost_list, ghost_total
    ghost_total = 0
    ghost_list.clear()
    image_position_x = 0
    image_position_y = 0
    for datas in range(y_line):
        for data in range(x_line):
            if tile_map[datas][data]=='g':
                ghost_num = screen.blit(ghost_down,(image_position_x,image_position_y))
                ghost_list.append(ghost_num)
                ghost_total = ghost_total + 1
            image_position_x += 50
        image_position_y += 50
        image_position_x = 0
    print(ghost_list)
ghost_setting()
######################################################### 


def ghost_move():
    global  monster_death

    for i in range(0,ghost_total):
        global ghost_face, move_count50
        

        result = ''
        ghost_x = int((ghost_list[i][0])/50)
        ghost_y = int((ghost_list[i][1])/50)

        ghost_move_list = []

        if tile_map[ghost_y][ghost_x+1] == 'o' :
            ghost_move_list.append('동')
        if tile_map[ghost_y][ghost_x-1] == 'o' :
            ghost_move_list.append('서')
        if tile_map[ghost_y+1][ghost_x] == 'o' :
            ghost_move_list.append('남')
        if tile_map[ghost_y-1][ghost_x] == 'o' :
            ghost_move_list.append('북')
        

        if ghost_move_list != [] :
            onemore = 0
            result = random.choice(ghost_move_list)
            if onemore == 0 : move_total_result.append(result)
            if move_count50 == 50 : 
                move_total_result.clear()
                move_total_result.append(result)
                move_count50 = 0
            if move_total_result[i] == '동' :
                ghost_list[i][0] = ghost_list[i][0] + 1
                ghost_face = ghost_right
            if move_total_result[i] == '서' :
                ghost_list[i][0] = ghost_list[i][0] - 1
                ghost_face = ghost_left
            if move_total_result[i] == '남' :
                ghost_list[i][1] = ghost_list[i][1] + 1
                ghost_face = ghost_down
            if move_total_result[i] == '북' :
                ghost_list[i][1] = ghost_list[i][1] - 1
                ghost_face = ghost_up
            screen.blit(ghost_face,ghost_list[i])
        else : 
            move_total_result.append('없음')
            ghost_face_random = [ghost_down, ghost_up, ghost_left, ghost_right]
            screen.blit(random.choice(ghost_face_random),ghost_list[i])

        if tile_map[ghost_y][ghost_x] == 't' :
            ghost_list[i][0] = 0
            ghost_list[i][1] = 0
            
            monster_death = monster_death + 1
            print(monster_death)

        if ghost_y == round(player_y_pos/50) and ghost_x == round(player_x_pos/50) :
            global restart
            restart = 1

    move_count50 = move_count50 + 1






# print(ghost_list[0][0]) => x좌표
# print(ghost_list[0][1]) => y좌표



######################################################### 
def runGame():
    while not done:
        # screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 게임 화면 종료
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        global player_x_pos, player_y_pos, bombman, bomb_click, test_count5, bomb_num, restart, restart_count, move_count50

        if restart == 1 : 

            if (keys[pygame.K_TAB]):
                player_y_pos = 50
                player_x_pos = 50
                restart = 0
                restart_count = 0

            if (keys[pygame.K_ESCAPE]):
                map_clear()
                ghost_setting()
                ghost_move()
                bomb_map.clear()
                map_bomb()

                move_count50 = 0
                player_y_pos = 50
                player_x_pos = 50
                restart = 0
                restart_count = 0
        else : 

            if (keys[pygame.K_LEFT]):
                if tile_map[math.ceil(player_y_pos/50)][(player_x_pos-1)//50] == 'x' or tile_map[player_y_pos//50][(player_x_pos-1)//50] == 'x':
                    ''
                elif tile_map[math.ceil(player_y_pos/50)][(player_x_pos-1)//50] == 'b' or tile_map[player_y_pos//50][(player_x_pos-1)//50] == 'b':
                    ''
                elif bomb_map[math.ceil(player_y_pos/50)][(player_x_pos-25)//50] == 'p' or bomb_map[player_y_pos//50][(player_x_pos-25)//50] == 'p':
                    ''
                else :
                    player_x_pos -= 5
                bombman = bombman_left

            if (keys[pygame.K_RIGHT]):
                if tile_map[math.ceil(player_y_pos/50)][math.ceil((player_x_pos+1)/50)] == 'x' or tile_map[player_y_pos//50][math.ceil((player_x_pos+1)/50)] == 'x':
                    ''
                elif tile_map[math.ceil(player_y_pos/50)][math.ceil((player_x_pos+1)/50)] == 'b' or tile_map[player_y_pos//50][math.ceil((player_x_pos+1)/50)] == 'b':
                    ''
                elif bomb_map[math.ceil(player_y_pos/50)][math.ceil((player_x_pos+1)/50)] == 'p' or bomb_map[player_y_pos//50][math.ceil((player_x_pos+1)/50)] == 'p':
                    ''
                else :   
                    player_x_pos += 5
                bombman = bombman_right

            if (keys[pygame.K_UP]):
                if tile_map[(player_y_pos-1)//50][math.ceil((player_x_pos)/50)] == 'x' or tile_map[(player_y_pos-1)//50][(player_x_pos)//50] == 'x':
                    '' 
                elif tile_map[(player_y_pos-1)//50][math.ceil((player_x_pos)/50)] == 'b' or tile_map[(player_y_pos-1)//50][(player_x_pos)//50] == 'b':
                    '' 
                elif bomb_map[(player_y_pos-25)//50][math.ceil((player_x_pos)/50)] == 'p' or bomb_map[(player_y_pos-25)//50][(player_x_pos)//50] == 'p':
                    '' 
                else : 
                    player_y_pos -= 5
                bombman = bombman_up

            if (keys[pygame.K_DOWN]):
                if tile_map[math.ceil((player_y_pos+1)/50)][math.ceil((player_x_pos)/50)] == 'x' or tile_map[math.ceil((player_y_pos+1)/50)][(player_x_pos)//50] == 'x':
                    ''
                elif tile_map[math.ceil((player_y_pos+1)/50)][math.ceil((player_x_pos)/50)] == 'b' or tile_map[math.ceil((player_y_pos+1)/50)][(player_x_pos)//50] == 'b':
                    ''
                elif bomb_map[math.ceil((player_y_pos+1)/50)][math.ceil((player_x_pos)/50)] == 'p' or bomb_map[math.ceil((player_y_pos+1)/50)][(player_x_pos)//50] == 'p':
                    ''
                else : 
                    player_y_pos += 5
                bombman = bombman_down
                
            if (keys[pygame.K_SPACE]):
                if bomb_num != bomb_limit : 
                    bomb_click = 1
                    count = test_count5
            schedule.run_pending()
            display_map()
            ghost_move()
            display_bomb_map()
            lose_game()
            clock.tick(30)
            pygame.display.update()
            # pygame.display.flip()
        
            
                


######################################################### 
runGame()
######################################################### 

