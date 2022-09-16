import os
from re import A, I
import pygame
import sys
import math
import random
import schedule
from datetime import datetime
from pygame.locals import *

######################################################### 

os.system("cls")
pygame.init()

dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir)

######################################################### 




######################################################### 기본 맵, 나열 맵, x축, y축 출력 map_open()
def map_open():
    map_txt = open('txt/bombman.txt', 'r', encoding='utf-8')
    global x_line, y_line, trans_map, origin_map
    origin_map = map_txt.read()                                             # 오리지날 맵   origin_map
    x_line = origin_map.replace(' ','').find('\n')                          # X라인 개수    x_line
    y_line = int(len(origin_map.replace(' ','').replace('\n',''))/x_line)   # Y라인 개수    y_line
    trans_map = origin_map.replace(' ','').replace('\n','')                 # 일자 맵       trans_map
    map_txt.close()
map_open()

######################################################### 기초 배열 맵 출력 map_clear()
tile_map = []
def map_clear():
    tile_map.clear()
    map_txt = open('txt/bombman.txt', 'r', encoding='utf-8')
    while True:
        line_map = map_txt.readline()
        if not line_map:
            break
        line_map = line_map.replace('\n','')
        clear_map = line_map.split(' ')
        tile_map.append(clear_map)                                          # 핵심 배열 맵  tile_map
    map_txt.close()
map_clear()
print(tile_map)
######################################################### 폭탄 배열 맵 출력 map_bomb() 빈값은 'o'로 출력
def map_bomb():
    global bomb_map
    bomb_map = [[0]*y_line for _ in range(y_line)]

    for a in range(y_line):
        for b in range(x_line):
            bomb_map[a][b] = tile_map[a][b]
        

    for a in range(y_line):
        for b in range(x_line):
            bomb_map[a][b] = 'o'                                            # 핵심 폭탄 맵  bomb_map
map_bomb()

######################################################### 파이게임 정보 입력
def setting():

    global screen, done, clock, size, tap_click
    size = [x_line*50, y_line*50]                                           # 맵 기준 사이즈 X,T
    done = False
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    tap_click = 0

    global player_x_pos, player_y_pos                       # 플레이어 위치 및 기준값
    player_x_pos = 50                   # 플레이어 X축 기본 처음 위치
    player_y_pos = 50                   # 플레이어 Y축 기본 처음 위치

    global bomb_count_list, bomb_position_list, bomb_count, bomb_click, bomb_num, boom_check
    bomb_count_list = []
    bomb_position_list = []
    bomb_click = 0              # SPACE 클릭시 폭탄을 나타내는 버튼
    boom_check = 0              # 폭탄이 터졌는지 확인하는 함수
    bomb_num = -1                # 폭탄 개수 제한 함수
    bomb_count = [0,0,0]        # 폭탄 위치 저장 함수   ([1번폭탄, 2번폭탄, 3번폭탄])

    global item_chance, player_speed, bomb_limit, bomb_power, item_limit
    item_limit = 20             # 한 게임에서 아이템 개수 제한
    item_chance = ['a','a','b','b','c'] 
    player_speed = 1            # 플레이어 스피드       (기본-1 맥스-2) c 
    bomb_limit = 1               # 폭탄 개수 조절        (기본-1 맥스-5) a
    bomb_power = 1                # 폭탄 파워 조절        (기본-1 맥스-5) b
    
    global restart, restart_count
    restart = 0
    restart_count = 0

    global ghost_num, ghost_list, ghost_total
    ghost_num = 0
    ghost_list = []
    ghost_total = 0

    global bax_list, bax_num, select_bax
    bax_num = 0
    bax_list =[]
    select_bax =[]

    global test_count5, move_count50, move_total_result, monster_death, move_boss_result, boss_hp
    test_count5=0
    move_count50 = 0
    move_count50 = 0
    move_total_result = []
    move_boss_result = []
    monster_death = 0
    boss_hp = 10

    global space_click
    space_click = 0

    global block, road, bomb, boom, box                                                   # 기초 배치 이미지
    block = pygame.transform.scale(pygame.image.load('image/block.png'), (50, 50))
    road = pygame.transform.scale(pygame.image.load('image/road_image.png'), (50, 50))
    box = pygame.transform.scale(pygame.image.load('image/box_image.png'), (50, 50))
    bomb = pygame.transform.scale(pygame.image.load('image/bomb_image.png'), (50, 50))
    boom = pygame.transform.scale(pygame.image.load('image/boom.gif'), (50, 50))

    global item_plus, item_power, item_speed                                              # 아이템 이미지
    item_plus = pygame.transform.scale(pygame.image.load('image/item_plus.png'), (50, 50))
    item_power = pygame.transform.scale(pygame.image.load('image/item_power.png'), (50, 50))
    item_speed = pygame.transform.scale(pygame.image.load('image/item_speed.png'), (50, 50))

    global bombman_down,bombman_up ,bombman_left,bombman_right                                       # 플레이어 시선 이미지
    bombman_down = pygame.transform.scale(pygame.image.load('image/bombman_down.png'), (50, 50))
    bombman_up = pygame.transform.scale(pygame.image.load('image/bombman_up.png'), (50, 50))
    bombman_left = pygame.transform.scale(pygame.image.load('image/bombman_left.png'), (50, 50))
    bombman_right = pygame.transform.scale(pygame.image.load('image/bombman_right.png'), (50, 50))
    
    global ghost_down,ghost_up ,ghost_left,ghost_right, ghost_face, ghost_boom, lose                             # 유령 시선 이미지
    ghost_down = pygame.transform.scale(pygame.image.load('image/ghost_down.png'), (50, 50))
    ghost_up = pygame.transform.scale(pygame.image.load('image/ghost_up.png'), (50, 50))
    ghost_left = pygame.transform.scale(pygame.image.load('image/ghost_left.png'), (50, 50))
    ghost_right = pygame.transform.scale(pygame.image.load('image/ghost_right.png'), (50, 50))
    ghost_boom = pygame.transform.scale(pygame.image.load('image/ghost_boom.png'), (50, 50))
    
    global boss_down,boss_up ,boss_left,boss_right, boss_face, boss_boom, lose, boss_speed                            # 유령 시선 이미지
    boss_down = pygame.transform.scale(pygame.image.load('image/ghost_down.png'), (100, 100))
    boss_up = pygame.transform.scale(pygame.image.load('image/ghost_up.png'), (100, 100))
    boss_left = pygame.transform.scale(pygame.image.load('image/ghost_left.png'), (100, 100))
    boss_right = pygame.transform.scale(pygame.image.load('image/ghost_right.png'), (100, 100))
    boss_boom = pygame.transform.scale(pygame.image.load('image/ghost_boom.png'), (100, 100))
    boss_speed = 1
    
    global lose                                                                                       # 기타 배경 이미지
    lose = pygame.transform.scale(pygame.image.load('image/lose.jpg'), (x_line*50, y_line*50))

    global image_1, image_2, image_3, image_4, image_5, image_6, image_7, image_8, image_9, image_10, image_11, image_12          # 기타 이미지    
    image_1 = pygame.transform.scale(pygame.image.load('image/1_image.png'), (50, 50))
    image_2 = pygame.transform.scale(pygame.image.load('image/2_image.png'), (50, 50))
    image_3 = pygame.transform.scale(pygame.image.load('image/3_image.png'), (50, 50))
    image_4 = pygame.transform.scale(pygame.image.load('image/4_image.png'), (50, 50))
    image_5 = pygame.transform.scale(pygame.image.load('image/5_image.png'), (50, 50))
    image_6 = pygame.transform.scale(pygame.image.load('image/6_image.png'), (50, 50))
    image_7 = pygame.transform.scale(pygame.image.load('image/7_image.png'), (50, 50))
    image_8 = pygame.transform.scale(pygame.image.load('image/8_image.png'), (50, 50))
    image_9 = pygame.transform.scale(pygame.image.load('image/9_image.png'), (50, 50))
    image_10 = pygame.transform.scale(pygame.image.load('image/10_image.png'), (50, 50))
    image_11 = pygame.transform.scale(pygame.image.load('image/11_image.png'), (50, 50))
    image_12 = pygame.transform.scale(pygame.image.load('image/12_image.png'), (50, 50))

    global bombman_face, ghost_face
    bombman_face = bombman_down         # 플레이어 시작 얼굴
    ghost_face = ghost_down             # 유령 시작 얼굴
    boss_face = boss_down
setting()

######################################################### 기초 고정 벽 및 길 배치
def display_map():
    for datas in range(y_line):
        for data in range(x_line):
            if tile_map[datas][data]=='o' or tile_map[datas][data]=='b' or tile_map[datas][data]=='m' or tile_map[datas][data]=='g':
                screen.blit(road,(data*50,datas*50))
            if tile_map[datas][data]=='x' or tile_map[datas][data]=='z':
                screen.blit(block,(data*50,datas*50))
            if tile_map[datas][data]=='t':
                tile_map[datas][data] ='o' 
            if monster_death > 0 and tile_map[datas][data]=='z':
                tile_map[datas][data] = 'o'
                screen.blit(road,(data*50,datas*50))
                

######################################################### 
def item_impormation():
    global bax_num, bax_list
    bax_num = trans_map.count('b')      # 배열 내 b(bax)의 개수
    for datas in range(y_line):
        for data in range(x_line):
            if tile_map[datas][data]=='b':
                bax_list.append([data,datas]) # 박스 리스트에 박스 위치값 나열

    for a in range(item_limit):
        bax_pos = random.choice(bax_list)
        select_bax.append(bax_pos)
        bax_list.remove(bax_pos)

    for a in range(len(select_bax)):
        if tile_map[select_bax[a][0]][select_bax[a][1]]=='b':
            screen.blit(item_plus,(select_bax[a][1]*50,select_bax[a][0]*50))
            bomb_map[select_bax[a][0]][select_bax[a][1]] = random.choice(item_chance)
item_impormation()
######################################################### 

def display_item():
    global bomb_limit, bomb_power, player_speed, bomb_map
    for datas in range(y_line):
        for data in range(x_line):
            if bomb_map[datas][data]=='a':
                screen.blit(item_plus,(data*50,datas*50))
                if player_x_pos//50 == data and player_y_pos//50 == datas:
                    screen.blit(road,(data*50,datas*50))
                    bomb_map[datas][data]='o'
                    if bomb_limit < 5:
                        bomb_limit = bomb_limit + 1
            if bomb_map[datas][data]=='b':
                screen.blit(item_power,(data*50,datas*50))
                if player_x_pos//50 == data and player_y_pos//50 == datas:
                    screen.blit(road,(data*50,datas*50))
                    bomb_map[datas][data]='o'
                    if bomb_power < 5:
                        bomb_power = bomb_power + 1
            if bomb_map[datas][data]=='c':
                screen.blit(item_speed,(data*50,datas*50))
                if player_x_pos/50 == data and player_y_pos/50 == datas:
                    screen.blit(road,(data*50,datas*50))
                    bomb_map[datas][data]='o'
                    if player_speed < 2:
                        player_speed = player_speed + 1
                


######################################################### 
def display_bax():
    for datas in range(y_line):
        for data in range(x_line):
            if tile_map[datas][data]=='b':
                screen.blit(box,(data*50,datas*50))
######################################################### 
def display_monster():
    global ghost_num, ghost_list, ghost_total, monster_death
    ghost_total = 0
    ghost_list.clear()
    for datas in range(y_line):
        for data in range(x_line):
            if tile_map[datas][data]=='m':
                ghost_num = screen.blit(ghost_down,(data*50,datas*50))
                ghost_list.append(ghost_num)
                ghost_total = ghost_total + 1
                tile_map[datas][data] ='o'
display_monster()
######################################################### 
def monster_move():

    for i in range(0,ghost_total):
        global ghost_face, move_count50, monster_death, move_total_result
        
        result = ''
        ghost_x = int((ghost_list[i][0])/50)
        ghost_y = int((ghost_list[i][1])/50)

        ghost_move_list = []
        try : 
            if tile_map[ghost_y][ghost_x+1] == 'o' and bomb_map[ghost_y][ghost_x+1] == 'o' :
                ghost_move_list.append('동')
            if tile_map[ghost_y][ghost_x-1] == 'o' and bomb_map[ghost_y][ghost_x-1] == 'o' :
                ghost_move_list.append('서')
            if tile_map[ghost_y+1][ghost_x] == 'o' and bomb_map[ghost_y+1][ghost_x] == 'o' :
                ghost_move_list.append('남')
            if tile_map[ghost_y-1][ghost_x] == 'o' and bomb_map[ghost_y-1][ghost_x] == 'o' :
                ghost_move_list.append('북')
        except IndexError:
            ''
        onemore = 0
        try :
            result = random.choice(ghost_move_list)
        except IndexError:
            ''
        if onemore == 0 : 
            move_total_result.append(result)
            onemore = 1
        if move_count50 == 50 : 
            move_total_result.clear()
            move_total_result.append(result)
            move_count50 = 0
            onemore = 0
        try :
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
            if move_total_result[i] == '' :
                ghost_face = ghost_down
        except IndexError:
            ''
        screen.blit(ghost_face,ghost_list[i])
        if ghost_list[i][0] == -50 :
            ghost_face_random = [ghost_down, ghost_up, ghost_left, ghost_right]
            screen.blit(random.choice(ghost_face_random),ghost_list[i])

        if tile_map[ghost_list[i][1]//50][ghost_list[i][0]//50] == 't' :
            move_total_result[i] = ''
            ghost_list[i][0] = -50
            ghost_list[i][1] = -50
            monster_death = monster_death + 1
            print(monster_death)
            
        if ghost_y == round(player_y_pos/50) and ghost_x == round(player_x_pos/50) :
            global restart
            restart = 1
            
    move_count50 = move_count50 + 1
######################################################### 
def display_boss():
    global boss_pos
    for datas in range(y_line):
        for data in range(x_line):
            if tile_map[datas][data]=='g':
                boss_pos = screen.blit(boss_down,(data*50,datas*50))
                tile_map[datas][data] ='o'
display_boss()
######################################################### 
def boss_move():

    global boss_face, move_count50, move_boss_result, boss_speed, boss_hp, boss_boom
    boss_move_list = []

    boss_x_pos = int(boss_pos[0]/50)
    boss_y_pos = int(boss_pos[1]/50)

    try : 
        if tile_map[boss_y_pos][boss_x_pos+2] == 'o' :
            boss_move_list.append('동')
        if tile_map[boss_y_pos][boss_x_pos-1] == 'o' :
            boss_move_list.append('서')
        if tile_map[boss_y_pos+2][boss_x_pos] == 'o' :
            boss_move_list.append('남')
        if tile_map[boss_y_pos-1][boss_x_pos] == 'o' :
            boss_move_list.append('북')
    except IndexError:
        ''

            
    if boss_move_list != [] :
        result = random.choice(boss_move_list)
        move_boss_result.append(result)
        if move_count50 == 50 : 
            move_boss_result.clear()
            move_boss_result.append(result)
            
        for a in range(20):
            if (boss_y_pos) == (player_y_pos)//50 and (boss_x_pos) + a == (player_x_pos)//50 and boss_pos[0]%50 == 0 and boss_face == boss_right:
                move_boss_result.clear()
                move_boss_result.append('동')
                boss_speed = 10
            if (boss_y_pos) == (player_y_pos)//50 and (boss_x_pos) - a == (player_x_pos)//50 and boss_pos[0]%50 == 0 and boss_face == boss_left:
                move_boss_result.clear()
                move_boss_result.append('서')
                boss_speed = 10
            if (boss_y_pos) + a == (player_y_pos)//50 and (boss_x_pos) == (player_x_pos)//50 and boss_pos[1]%50 == 0 and boss_face == boss_up:
                move_boss_result.clear()
                move_boss_result.append('남')
                boss_speed = 10
            if (boss_y_pos) - a == (player_y_pos)//50 and (boss_x_pos) == (player_x_pos)//50 and boss_pos[1]%50 == 0 and boss_face == boss_down:
                move_boss_result.clear()
                move_boss_result.append('북')
                boss_speed = 10
                
        if boss_speed > 1:
            boss_speed = boss_speed -1
                
        if move_boss_result[0] == '동' :
            boss_pos[0] = boss_pos[0] + boss_speed
            boss_face = boss_right
        if move_boss_result[0] == '서' :
            boss_pos[0] = boss_pos[0] - boss_speed
            boss_face = boss_left
        if move_boss_result[0] == '남' :
            boss_pos[1] = boss_pos[1] + boss_speed
            boss_face = boss_down
        if move_boss_result[0] == '북' :
            boss_pos[1] = boss_pos[1] - boss_speed
            boss_face = boss_up
        screen.blit(boss_face,boss_pos)
    else : 
        move_boss_result.append('없음')
        boss_face_random = [boss_down, boss_up, boss_left, boss_right]
        screen.blit(random.choice(boss_face_random),boss_pos)

        if tile_map[boss_y_pos][boss_x_pos] == 't' and monster_death == 10:
            boss_hp = boss_hp - 1
            boss_face = boss_boom
            pygame.transform.scale(pygame.image.load('image/ghost_boom.png'), (100, 100))
            if boss_hp == 0:
                print("승리")
            
            
        

    if boss_y_pos == round(player_y_pos/50) and boss_x_pos == round(player_x_pos/50) :
        global restart
        restart = 1

    

######################################################### 
def display_player():
    global restart
    if restart == 0 : 
        screen.blit(bombman_face,(player_x_pos,player_y_pos))
        
######################################################### 시작 후 게임 초당 값 생성
def test_1Sec():
    global test_count5
    test_count5 +=1
    ## print(f"{test_count5}")
    return test_count5
test_1Sec()
schedule.every(0.1).seconds.do(test_1Sec)

######################################################### 스페이스 클릭 시 폭탄 생성 및 폭팔
def bomb_impormation():
    global bomb_click, bomb_count_list, bomb_position_list, bomb_num
    if bomb_click == 1:
        bomb_x = round(player_x_pos/50)*50

        bomb_y = round(player_y_pos/50)*50

        if bomb_map[int(bomb_y/50)][int(bomb_x/50)] =='o' and bomb_num < bomb_limit:
            bomb_num = bomb_num + 1
            bomb_count_list.append(test_count5)
            bomb_position_list.append([bomb_x,bomb_y])
        bomb_click = 0
                                

######################################################### 
def display_bomb():
    global bomb_count_list, bomb_position_list, bomb_num, boom_check, restart, player_x_pos, player_y_pos
    for num in range(len(bomb_count_list)):

        bomb_count_down = 20 ## 폭탄 카운트 몇초로 할지(/10)

        if bomb_count_list[num] + bomb_count_down == test_count5:
            screen.blit(boom,(bomb_position_list[num][0],bomb_position_list[num][1]))
            if int(bomb_position_list[num][1])//50 == player_y_pos//50 and int(bomb_position_list[num][0])//50 == player_x_pos//50:
                restart = 1
            bomb_map[int(bomb_position_list[num][1])//50][int(bomb_position_list[num][0])//50] = 'o'
            boom_right_end = 0
            boom_left_end = 0
            boom_down_end = 0
            boom_up_end = 0
            for n in range(bomb_power):
                n = n + 1
                if boom_right_end == 0:
                    try :
                        if tile_map[int(bomb_position_list[num][1])//50][int((bomb_position_list[num][0])//50) + n] != 'x':
                            tile_map[int(bomb_position_list[num][1])//50][int((bomb_position_list[num][0])//50) + n] = 't'
                            screen.blit(boom,(bomb_position_list[num][0] + (n*50),bomb_position_list[num][1]))
                        else : boom_right_end = 1
                    except IndexError:
                        ''
                if boom_left_end == 0:
                    if tile_map[int(bomb_position_list[num][1])//50][int((bomb_position_list[num][0])//50) - n] != 'x':
                        tile_map[int(bomb_position_list[num][1])//50][int((bomb_position_list[num][0])//50) - n] = 't'
                        screen.blit(boom,(bomb_position_list[num][0] - (n*50),bomb_position_list[num][1]))
                    else : boom_left_end = 1
                if boom_down_end == 0:
                    try :
                        if tile_map[int((bomb_position_list[num][1])//50) + n][int((bomb_position_list[num][0])//50)] != 'x':
                            tile_map[int((bomb_position_list[num][1])//50) + n][int((bomb_position_list[num][0])//50)] = 't'
                            screen.blit(boom,(bomb_position_list[num][0],bomb_position_list[num][1] + (n*50)))
                        else : boom_down_end = 1
                    except IndexError:
                        ''
                if boom_up_end == 0:
                    if tile_map[int((bomb_position_list[num][1])//50) - n][int((bomb_position_list[num][0])//50)] != 'x':
                        tile_map[int((bomb_position_list[num][1])//50) - n][int((bomb_position_list[num][0])//50)] = 't'
                        screen.blit(boom,(bomb_position_list[num][0],bomb_position_list[num][1] - (n*50)))
                    else : boom_up_end = 1
            if tile_map[player_y_pos//50][player_x_pos//50] == 't': 
                restart = 1
                    
            
            boom_check = 1

        if bomb_count_list[num] + bomb_count_down == test_count5 + 1:
            bomb_map[int(bomb_position_list[num][1])//50][int(bomb_position_list[num][0])//50] = 'o'
            screen.blit(road,(bomb_position_list[num][0],bomb_position_list[num][1]))
            if boom_check == 1 : 
                bomb_num = bomb_num -1
                boom_check = 0
            
        if bomb_count_list[num] <= test_count5 and test_count5 - bomb_count_list[num] < bomb_count_down :
            screen.blit(bomb,(bomb_position_list[num][0],bomb_position_list[num][1]))
            bomb_map[int(bomb_position_list[num][1])//50][int(bomb_position_list[num][0])//50] = 'p'






######################################################### 
def tap_on():
    pygame.draw.rect(screen, (0, 0, 0), [x_line*50,0,100,y_line*50])
    pygame.draw.circle(screen, (255,255,255), [(x_line*50) + 50,50],40)
    screen.blit(bombman_face,((x_line*50) + 25, 25))   
    screen.blit(item_plus,((x_line*50) + 25, 125))   
    if bomb_limit == 1 :screen.blit(image_1,((x_line*50) + 25, 200))   
    if bomb_limit == 2 :screen.blit(image_2,((x_line*50) + 25, 200))   
    if bomb_limit == 3 :screen.blit(image_3,((x_line*50) + 25, 200))  
    if bomb_limit == 4 :screen.blit(image_4,((x_line*50) + 25, 200))   
    if bomb_limit == 5 :screen.blit(image_5,((x_line*50) + 25, 200)) 
      
    screen.blit(item_power,((x_line*50) + 25, 275))   
    if bomb_power == 1 :screen.blit(image_1,((x_line*50) + 25, 350)) 
    if bomb_power == 2 :screen.blit(image_2,((x_line*50) + 25, 350)) 
    if bomb_power == 3 :screen.blit(image_3,((x_line*50) + 25, 350)) 
    if bomb_power == 4 :screen.blit(image_4,((x_line*50) + 25, 350)) 
    if bomb_power == 5 :screen.blit(image_5,((x_line*50) + 25, 350)) 
       
    screen.blit(item_speed,((x_line*50) + 25, 425))  
    if player_speed == 1 :screen.blit(image_1,((x_line*50) + 25, 500)) 
    if player_speed == 2 :screen.blit(image_2,((x_line*50) + 25, 500)) 
    if player_speed == 3 :screen.blit(image_3,((x_line*50) + 25, 500)) 
    
    if monster_death == 0 :
        screen.blit(ghost_boom,((x_line*50) + 25, 575))
    else : 
        screen.blit(ghost_down,((x_line*50) + 25, 575))  
    
    if monster_death == 0 :screen.blit(image_10,((x_line*50) + 25, 650)) 
    if monster_death == 1 :screen.blit(image_9,((x_line*50) + 25, 650)) 
    if monster_death == 2 :screen.blit(image_8,((x_line*50) + 25, 650)) 
    if monster_death == 3 :screen.blit(image_7,((x_line*50) + 25, 650)) 
    if monster_death == 4 :screen.blit(image_6,((x_line*50) + 25, 650)) 
    if monster_death == 5 :screen.blit(image_5,((x_line*50) + 25, 650)) 
    if monster_death == 6 :screen.blit(image_4,((x_line*50) + 25, 650)) 
    if monster_death == 7 :screen.blit(image_3,((x_line*50) + 25, 650)) 
    if monster_death == 8 :screen.blit(image_2,((x_line*50) + 25, 650)) 
    if monster_death == 9 :screen.blit(image_1,((x_line*50) + 25, 650)) 
     
######################################################### 
def restart_choice():  
    screen.blit(lose,(0, 0))

######################################################### 게임 전체 시작 함수

def runGame():
    while not done:
        global player_x_pos, player_y_pos, space_click, bombman_face, bomb_click, size, tap_click, restart, move_count50, bomb_limit, bomb_power, player_speed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 게임 화면 종료
                pygame.quit()
                sys.exit()
            keys = pygame.key.get_pressed()

            if (keys[pygame.K_SPACE]):
                space_click += 1
                if space_click == 2 :
                    bomb_click = 1
                    space_click = 0
                    

            if (keys[pygame.K_TAB]):
                print("z")
                size = [x_line*50 + 2*50, y_line*50]   
                screen = pygame.display.set_mode(size)
                if restart == 1:  
                    player_x_pos = 50
                    player_y_pos = 50
                    restart = 0

                      
            if (keys[pygame.K_ESCAPE]):
                if restart == 1 :
                    player_x_pos = 50
                    player_y_pos = 50
                    monster_death = 0
                    map_clear()
                    item_impormation()
                    display_monster()
                    display_boss()
                    player_speed = 1            
                    bomb_limit = 1               
                    bomb_power = 1
                    move_count50 = 0
                    move_boss_result.clear()
                    move_total_result.clear()
                    restart = 0

        if (keys[pygame.K_LEFT]):
            if   tile_map[math.ceil(player_y_pos/50)][(player_x_pos - 1*player_speed)//50] == 'x' or tile_map[player_y_pos//50][(player_x_pos - 1*player_speed)//50] == 'x':
                ''
            elif tile_map[math.ceil(player_y_pos/50)][(player_x_pos - 1*player_speed)//50] == 'b' or tile_map[player_y_pos//50][(player_x_pos - 1*player_speed)//50] == 'b':
                ''
            elif bomb_map[math.ceil(player_y_pos/50)][(player_x_pos - 1*player_speed)//50] == 'p' or bomb_map[player_y_pos//50][(player_x_pos - 1*player_speed)//50] == 'p':
                if bomb_map[math.ceil(player_y_pos/50)][(player_x_pos)//50] == 'p' or bomb_map[player_y_pos//50][(player_x_pos)//50] == 'p':
                    player_x_pos -= 5*player_speed
            else :
                player_x_pos -= 5*player_speed
            bombman_face = bombman_left

        if (keys[pygame.K_RIGHT]):
            if   tile_map[math.ceil(player_y_pos/50)][math.ceil((player_x_pos + 1*player_speed)/50)] == 'x' or tile_map[player_y_pos//50][math.ceil((player_x_pos + 1*player_speed)/50)] == 'x':
                ''
            elif tile_map[math.ceil(player_y_pos/50)][math.ceil((player_x_pos + 1*player_speed)/50)] == 'b' or tile_map[player_y_pos//50][math.ceil((player_x_pos + 1*player_speed)/50)] == 'b':
                ''
            elif bomb_map[math.ceil(player_y_pos/50)][math.ceil((player_x_pos + 1*player_speed)/50)] == 'p' or bomb_map[player_y_pos//50][math.ceil((player_x_pos + 1*player_speed)/50)] == 'p':
                if bomb_map[math.ceil(player_y_pos/50)][math.ceil((player_x_pos)/50)] == 'p' or bomb_map[player_y_pos//50][math.ceil((player_x_pos)/50)] == 'p':
                    player_x_pos += 5*player_speed
            else :   
                player_x_pos += 5*player_speed
            bombman_face = bombman_right

        if (keys[pygame.K_UP]):
            if   tile_map[(player_y_pos - 1*player_speed)//50][math.ceil((player_x_pos)/50)] == 'x' or tile_map[(player_y_pos - 1*player_speed)//50][(player_x_pos)//50] == 'x':
                '' 
            elif tile_map[(player_y_pos - 1*player_speed)//50][math.ceil((player_x_pos)/50)] == 'b' or tile_map[(player_y_pos - 1*player_speed)//50][(player_x_pos)//50] == 'b':
                '' 
            elif bomb_map[(player_y_pos - 1*player_speed)//50][math.ceil((player_x_pos)/50)] == 'p' or bomb_map[(player_y_pos - 1*player_speed)//50][(player_x_pos)//50] == 'p':
                if bomb_map[(player_y_pos)//50][math.ceil((player_x_pos)/50)] == 'p' or bomb_map[(player_y_pos)//50][(player_x_pos)//50] == 'p':
                    player_y_pos -= 5*player_speed
            else : 
                player_y_pos -= 5*player_speed
            bombman_face = bombman_up

        if (keys[pygame.K_DOWN]):
            if   tile_map[math.ceil((player_y_pos + 1*player_speed)/50)][math.ceil((player_x_pos)/50)] == 'x' or tile_map[math.ceil((player_y_pos + 1*player_speed)/50)][(player_x_pos)//50] == 'x':
                ''
            elif tile_map[math.ceil((player_y_pos + 1*player_speed)/50)][math.ceil((player_x_pos)/50)] == 'b' or tile_map[math.ceil((player_y_pos + 1*player_speed)/50)][(player_x_pos)//50] == 'b':
                ''
            elif bomb_map[math.ceil((player_y_pos + 1*player_speed)/50)][math.ceil((player_x_pos)/50)] == 'p' or bomb_map[math.ceil((player_y_pos + 1*player_speed)/50)][(player_x_pos)//50] == 'p':
                if bomb_map[math.ceil((player_y_pos)/50)][math.ceil((player_x_pos)/50)] == 'p' or bomb_map[math.ceil((player_y_pos)/50)][(player_x_pos)//50] == 'p':
                    player_y_pos += 5*player_speed
            else : 
                player_y_pos += 5*player_speed
            bombman_face = bombman_down

        display_map()
        display_item()
        display_bax()
        bomb_impormation()
        display_bomb()
        monster_move()
        boss_move()
        display_player()
        tap_on()
        if restart == 1 : restart_choice()
        clock.tick(30)
        schedule.run_pending()
        pygame.display.update()



##
## x = 벽 (넘을수 없음)
## o = 길 (움직일수 있음)
## b = 박스 (부실수 있음)
## m = 몬스터
##
##
##
##
##
##
##
##
##
##
##
##
##

runGame()
