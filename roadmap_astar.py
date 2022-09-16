import os
from re import X
import pygame
import sys
import time

os.system("cls")
pygame.init()

dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir)

## 기초 세팅
def setting():
    global xline_num, yline_num, one_pixel_size, big_font, middle_font, small_font, my_big_font, my_middle_font, my_small_font, xline_size, yline_size
    xline_num = 10          ## X라인 개수
    yline_num = 10          ## Y라인 개수
    one_pixel_size = 50     ## X,Y축 길이
    big_font = 70
    middle_font = 35
    small_font = 20
    my_big_font = pygame.font.SysFont(None,big_font)
    my_middle_font = pygame.font.SysFont(None,middle_font)
    my_small_font = pygame.font.SysFont(None,small_font)
    xline_size = one_pixel_size * xline_num
    yline_size = one_pixel_size * yline_num
    
    global tile_map, node_map, area_map, tile_map_view, node_map_view, area_map_view, help_size, imformation_click_all, result_inf ## 수정 안하는게 좋음
    help_size = 300         ## 도움말(help)창 너비 조절
    tile_map = []
    node_map = []
    area_map = []
    tile_map_view = 1
    node_map_view = 0
    area_map_view = 0
    imformation_click_all = [1,0,0,0,0,0]
    result_inf = ["",""]
    
    global next_pos, prev_pos, pass_pos, pos_f, pos_g, pos_h, click_check, move_ready
    next_pos = []
    prev_pos = []
    pass_pos = []
    pos_f = []
    pos_g = []
    pos_h = []
    click_check = 0
    move_ready = []
    
    global done, clock, screen
    size = [xline_num*one_pixel_size + help_size, yline_num*one_pixel_size]
    done = False
    screen = pygame.display.set_mode(size)
    screen.fill([255,255,255])
    clock = pygame.time.Clock()
    
    global start_xline, start_yline, end_xline, end_yline, start_check, end_check, map_click_lock, run_start, end_start, once_check
    start_xline = 0
    start_yline = 0
    end_xline = 0
    end_yline = 0
    start_check = 0
    end_check = 0
    map_click_lock = 0
    run_start = 0
    end_start = 0
    once_check = 0
    
    global distance_yline, distance_xline
    distance_yline  = 0
    distance_xline  = 0
setting()

## 맵 변경 리셋 함수
def display_map_reset():
    global node_map_view, tile_map_view, area_map_view
    tile_map_view = 0
    node_map_view = 0
    area_map_view = 0    
    
## 도움말 창 변경 메세지 내용 입력
def help_massage_main():
    global message0, message1, message2, message3, message4, message5, message6, help_choice
    all_massage = ["HELP","Click Lock","Change Map","Run Astar","","","Reset"]
    all_massage_color = [(255,255,255),(255,255,255),(255,255,255),(255,255,255),(0,0,255),(0,255,255),(255,0,0)]
    message0 =    my_big_font.render(all_massage[0],True,all_massage_color[0])
    message1 = my_middle_font.render(all_massage[1],True,all_massage_color[1])
    message2 = my_middle_font.render(all_massage[2],True,all_massage_color[2])
    message3 = my_middle_font.render(all_massage[3],True,all_massage_color[3])
    message4 = my_middle_font.render(all_massage[4],True,all_massage_color[4])
    message5 = my_middle_font.render(all_massage[5],True,all_massage_color[5])
    message6 = my_middle_font.render(all_massage[6],True,all_massage_color[6])
    help_choice = [message1,message2,message3,message4,message5,message6]
help_massage_main()      
def help_message_inf2():
    global inpormation_2_0, inpormation_2_1, inpormation_2_1, inpormation_2_2, inpormation_2_3, inpormation_2_4, inpormation_2_5, inpormation_2_6, help_inpormation_choice_2
    inpormation_2_0 =    my_big_font.render("MAP",True,(255,255,255))
    inpormation_2_1 = my_middle_font.render("tile map view",True,(255,255,255))
    inpormation_2_2 = my_middle_font.render("node map view",True,(255,255,0))
    inpormation_2_3 = my_middle_font.render("Area map view",True,(0,255,0))
    inpormation_2_4 = my_middle_font.render("",True,(0,0,255))
    inpormation_2_5 = my_middle_font.render("",True,(255,255,0))
    inpormation_2_6 = my_middle_font.render("back",True,(0,255,255))
    help_inpormation_choice_2 = [inpormation_2_1,inpormation_2_2,inpormation_2_3,inpormation_2_4,inpormation_2_5,inpormation_2_6]
help_message_inf2()    
def help_message_inf3():
    global inpormation_3_0, inpormation_3_1, inpormation_3_1, inpormation_3_2, inpormation_3_3, inpormation_3_4, inpormation_3_5, inpormation_3_6, help_inpormation_choice_3
    inpormation_3_0 =    my_big_font.render("Astar",True,(255,255,255))
    inpormation_3_1 = my_middle_font.render("1.Run Check",True,(255,255,255))
    inpormation_3_2 = my_middle_font.render("2-1.Run onec",True,(255,0,0))
    inpormation_3_3 = my_middle_font.render("2-2.Run all",True,(0,255,0))
    inpormation_3_4 = my_middle_font.render(result_inf[0],True,(0,0,255))
    inpormation_3_5 = my_middle_font.render(result_inf[1],True,(255,255,0))
    inpormation_3_6 = my_middle_font.render("back",True,(0,255,255))
    help_inpormation_choice_3 = [inpormation_3_1,inpormation_3_2,inpormation_3_3,inpormation_3_4,inpormation_3_5,inpormation_3_6]
help_message_inf3()

## 계속해서 변경되는 area 맵
def display_area_map():
    for yline in range(yline_num):
        for xline in range(xline_num):
            if area_map[yline][xline] == 'E':
                pygame.draw.rect(screen,[200,20,20],(one_pixel_size * xline+1,one_pixel_size * yline+1,one_pixel_size-2,one_pixel_size-2))
            if area_map[yline][xline] == 'B':
                pygame.draw.rect(screen,[200,200,200],(one_pixel_size * xline+1,one_pixel_size * yline+1,one_pixel_size-2,one_pixel_size-2))
            if area_map[yline][xline] == 'X':
                pygame.draw.rect(screen,[100,100,100],(one_pixel_size * xline+1,one_pixel_size * yline+1,one_pixel_size-2,one_pixel_size-2))
            if area_map[yline][xline] == 'N':
                pygame.draw.rect(screen,[100,100,255],(one_pixel_size * xline+1,one_pixel_size * yline+1,one_pixel_size-2,one_pixel_size-2),3)
            if area_map[yline][xline] == 'G':
                pygame.draw.rect(screen,[20,100,20],(one_pixel_size * xline+1,one_pixel_size * yline+1,one_pixel_size-2,one_pixel_size-2))
                pygame.draw.rect(screen,[100,100,255],(one_pixel_size * xline+1,one_pixel_size * yline+1,one_pixel_size-2,one_pixel_size-2),5)
    if area_map[yline][xline] == 'E' : 
        area_map[yline][xline] = 'X'   

## 터미널 사용 처음 맵 생성기(수정X)
def make_terminal_map():
    tile_map.clear()
    node_map.clear()
    area_map.clear()
    for yline in range(yline_num):
        etc_map = []
        etc_map2 = []
        etc_map3 = []
        for xline in range(xline_num):
            etc_map.append('O')
            etc_map2.append(0)
            etc_map3.append('□')
        tile_map.append('O')
        node_map.append(0)
        area_map.append('□')
        tile_map[yline] = etc_map
        node_map[yline] = etc_map2
        area_map[yline] = etc_map3
make_terminal_map()

## 도움말(help) 디스플레이 적용 함수(수정X)
def display_help():
    for a in range(6):
        imformation_click_all[a] = 0
    imformation_click_all[0]= 1
    pygame.draw.rect(screen,[0,0,0],(xline_size, 0, help_size, yline_size))
    pygame.draw.rect(screen,[20,20,20],(xline_size + 10, 10, help_size - 20, yline_size - 20))
    if imformation_click_all[0] == 1 : screen.blit(message0, (xline_size + (help_size/2) - 70, (yline_size - 20) / 7))
    for num in range(6):
        pygame.draw.rect(screen,[50,50,50],   (xline_size +(help_size/2) - 100 , 150 + (50*num),200,40))
        pygame.draw.rect(screen,[100,100,100],(xline_size +(help_size/2) - 100 , 150 + (50*num),200,40),2)
        if imformation_click_all[0] == 1 : screen.blit(help_choice[num], (xline_size +(help_size/3.6) - 20, 158 + (50*num))) 
display_help()    

## 터미널 창 현재 수정되는 상황 디스플레이
def display_terminal_map():
    if tile_map_view   == 1 : print("타일 맵(tile_map)")
    elif node_map_view == 1 : print("노드 맵(node_map)")
    elif area_map_view == 1 : print("지역 맵(area_map)")
    for yline in range(yline_num):
        for xline in range(xline_num):
            if tile_map_view   == 1 : print(tile_map[yline][xline], end=' ')
            elif node_map_view == 1 : print(node_map[yline][xline], end=' ')
            elif area_map_view == 1 : print(area_map[yline][xline], end=' ')
        print()
display_terminal_map()

## 파이게임 창 현재 수정되는 상황 디스플레이
def view_pygame_map():
    for yline in range(yline_num):
        for xline in range(xline_num):
            if tile_map[yline][xline] == 'O' :
                pygame.draw.rect(screen,[0,0,0],       (one_pixel_size * xline+1,one_pixel_size * yline+1,one_pixel_size-2,one_pixel_size-2))
            if tile_map[yline][xline] == 'X' :
                pygame.draw.rect(screen,[100,100,100], (one_pixel_size * xline+1,one_pixel_size * yline+1,one_pixel_size-2,one_pixel_size-2))
            if tile_map[yline][xline] == 'S' :
                pygame.draw.rect(screen,[20,100,20],   (one_pixel_size * xline+1,one_pixel_size * yline+1,one_pixel_size-2,one_pixel_size-2))
            if tile_map[yline][xline] == 'E' :
                pygame.draw.rect(screen,[200,20,20],   (one_pixel_size * xline+1,one_pixel_size * yline+1,one_pixel_size-2,one_pixel_size-2))
            if area_map[yline][xline] == 'o' :
                pygame.draw.rect(screen,[0,200,0],     (one_pixel_size * xline+1,one_pixel_size * yline+1,one_pixel_size-2,one_pixel_size-2))
            if run_start == 1 :
                if area_map[yline][xline] == '■' :
                    pygame.draw.rect(screen,[20,20,100],   (one_pixel_size * xline+1,one_pixel_size * yline+1,one_pixel_size-2,one_pixel_size-2))
                if area_map[yline][xline] == '▲' :
                    pygame.draw.rect(screen,[215,200,30],   (one_pixel_size * xline+1,one_pixel_size * yline+1,one_pixel_size-2,one_pixel_size-2), 3)
                if area_map[yline][xline] == '○' :
                    pygame.draw.rect(screen,[100,100,255], (one_pixel_size * xline+1,one_pixel_size * yline+1,one_pixel_size-2,one_pixel_size-2), 3)
                if area_map[yline][xline] == '●' :
                    pygame.draw.rect(screen,[200,20,20],   (one_pixel_size * xline+1,one_pixel_size * yline+1,one_pixel_size-2,one_pixel_size-2))
            if end_start == 1 :        
                if area_map[yline][xline] == 'V' :
                    pygame.draw.circle(screen,(200,50,50),(one_pixel_size * xline+25,one_pixel_size * yline+25),10)
            
                
## 도움말(help)창 클릭 실행 관리 
def mouse_click_help(event):
    global node_map_view, tile_map_view, area_map_view, map_click_lock
    help_row_index    = event.pos[0]
    help_column_index = (event.pos[1] - 150)//50
    os.system("cls")    
    try : 
        if help_row_index >= 550 and help_row_index <= 750:
            if imformation_click_all[0] == 1 : 
                if help_column_index == 0:
                    if imformation_click_all[0] == 1 : 
                        if map_click_lock == 0:
                            map_click_lock = 1
                        elif map_click_lock == 1:
                            map_click_lock = 0
                if help_column_index == 1:
                    if imformation_click_all[0] == 1 : 
                        display_help_impormation_2()
                if help_column_index == 2:
                    if imformation_click_all[0] == 1 : 
                        map_click_lock = 1
                        display_help_impormation_3()
                if help_column_index == 3:
                    if imformation_click_all[0] == 1 : ''
                if help_column_index == 4:
                    if imformation_click_all[0] == 1 : ''
                if help_column_index == 5:
                    if imformation_click_all[0] == 1 : 
                        setting()
                        display_help()  
                        make_terminal_map()
                
            elif imformation_click_all[1] == 1 :  
                if help_column_index == 0:
                    if imformation_click_all[1] == 1 : 
                        display_map_reset()
                        tile_map_view = 1
                if help_column_index == 1:
                    if imformation_click_all[1] == 1 : 
                        display_map_reset()
                        node_map_view = 1
                if help_column_index == 2:
                    if imformation_click_all[1] == 1 : 
                        display_map_reset()
                        area_map_view = 1
                if help_column_index == 3:
                    if imformation_click_all[1] == 1 : ''
                if help_column_index == 4:
                    if imformation_click_all[1] == 1 : ''
                if help_column_index == 5:
                    if imformation_click_all[1] == 1 : 
                        imformation_click_all[1] = 0
                        display_help() 
                        
            elif imformation_click_all[2] == 1 :  
                if help_column_index == 0:
                    if imformation_click_all[2] == 1 : 
                        display_map_reset()
                        area_map_view = 1
                        distance_check()
                        map_click_lock = 1
                if help_column_index == 1:
                    if imformation_click_all[2] == 1 : ''
                if help_column_index == 2:
                    if imformation_click_all[2] == 1 : ''
                if help_column_index == 3:
                    if imformation_click_all[2] == 1 : ''
                if help_column_index == 4:
                    if imformation_click_all[2] == 1 : ''
                if help_column_index == 5:
                    if imformation_click_all[2] == 1 : 
                        imformation_click_all[2] = 0
                        display_help() 
                    
    except IndexError:
        print("에러")
    display_terminal_map()

## 2번째 메뉴 클릭시 변환 실행
def display_help_impormation_2():
    for a in range(6):
        imformation_click_all[a] = 0
    imformation_click_all[1]= 1
    pygame.draw.rect(screen,[0,0,0],(xline_size, 0, help_size, yline_size))
    pygame.draw.rect(screen,[20,20,20],(xline_size + 10, 10, help_size - 20, yline_size - 20))
    screen.blit(inpormation_2_0, (xline_size + (help_size/2) - 70, (yline_size - 20) / 7))
    for num in range(6):
        pygame.draw.rect(screen,[50,50,50],       (xline_size +(help_size/2) - 100 , 150 + (50*num),200,40))
        pygame.draw.rect(screen,[100,100,100],    (xline_size +(help_size/2) - 100 , 150 + (50*num),200,40),2)
        screen.blit(help_inpormation_choice_2[num], (xline_size +(help_size/3.6) - 20, 158 + (50*num))) 
        
## 3번째 메뉴 클릭시 변환 실행
def display_help_impormation_3():
    for a in range(6):
        imformation_click_all[a] = 0
    imformation_click_all[2]= 1
    pygame.draw.rect(screen,[0,0,0],(xline_size, 0, help_size, yline_size))
    pygame.draw.rect(screen,[20,20,20],(xline_size + 10, 10, help_size - 20, yline_size - 20))
    screen.blit(inpormation_3_0, (xline_size + (help_size/2) - 70, (yline_size - 20) / 7))
    for num in range(6):
        pygame.draw.rect(screen,[50,50,50],       (xline_size +(help_size/2) - 100 , 150 + (50*num),200,40))
        pygame.draw.rect(screen,[100,100,100],    (xline_size +(help_size/2) - 100 , 150 + (50*num),200,40),2)
        screen.blit(help_inpormation_choice_3[num], (xline_size +(help_size/3.6) - 20, 158 + (50*num))) 
            
## 마우스 클릭시 수정
def mouse_click_map(event):
    global start_check, end_check
    row_index         = event.pos[0] // one_pixel_size
    column_index      = event.pos[1] // one_pixel_size
    os.system("cls")
    for y in range(10):
        for x in range(10):
            if tile_map[y][x].count('S') == 1:
                start_check = 1
            if tile_map[y][x].count('E') == 1:
                end_check = 1
    try : 
        if tile_map[column_index][row_index] == 'O' :
            tile_map[column_index][row_index] = 'X'
            area_map[column_index][row_index] = '■'
        elif tile_map[column_index][row_index] == 'X' and start_check == 0:
            tile_map[column_index][row_index] = 'S'
            area_map[column_index][row_index] = '■'
        elif tile_map[column_index][row_index] == 'X' and start_check == 1 and end_check == 1:
            tile_map[column_index][row_index] = 'O'
            area_map[column_index][row_index] = 'ㅁ'
        elif tile_map[column_index][row_index] == 'X' and start_check == 1:
            tile_map[column_index][row_index] = 'E'
            area_map[column_index][row_index] = '●'
        elif tile_map[column_index][row_index] == 'S' and end_check == 0 :
            start_check = 0
            tile_map[column_index][row_index] = 'E'
            area_map[column_index][row_index] = '●'
        elif tile_map[column_index][row_index] == 'S' and end_check == 1 :
            start_check = 0
            tile_map[column_index][row_index] = 'O'
            area_map[column_index][row_index] = '□'
        elif tile_map[column_index][row_index] == 'E' :
            end_check = 0
            tile_map[column_index][row_index] = 'O'
            area_map[column_index][row_index] = '□'
    except IndexError:
        ''
    display_terminal_map()

## 목적지 도착지 입력 완료 후 거리 체크 실행
def distance_check():
    global distance_xline, distance_yline, start_xline, start_yline, end_xline, end_yline, move_xline, move_yline
    for yline in range(yline_num):
        for xline in range(xline_num):
            if tile_map[yline][xline] =='S':
                start_xline = xline
                start_yline = yline
            if tile_map[yline][xline] =='E':
                end_xline = xline
                end_yline = yline
    try : 
        distance_xline = end_xline - start_xline 
        distance_yline = end_yline - start_yline 
    except UnboundLocalError:
        print("에러 : 시작 및 도착 값이 지도에 표기되어있지 않습니다")
    pass_pos.append([start_yline,start_xline])
    move_xline = start_xline
    move_yline = start_yline
## 에이스타 알고리즘 한턴 런

def tab_click_check():
    print("1 거리당 10 으로 계산함(보기좋게) ")
    print('X라인 거리 =',distance_xline*10)
    print('Y라인 거리 =',distance_yline*10)
    print('시작  위치 = (',start_xline*10,',',start_yline*10,")")
    print('도착  위치 = (',end_xline*10,',',end_yline*10,")")
    
def astar_algorizm():
    #     f(n) = g(n) + h(n)
    # f = 출발 지점에서 목적지까지의 총 비용
    # g = 현재 노드에서 출발 지점까지 총 비용
    # h = heuristic(휴리스틱), 현재 노드에서 목적지까지의 추정거리
    global move_xline, move_yline, click_check, run_start
    os.system("cls")
    run_start = 1
    if end_start == 0:
        if click_check == 0:
            area_map[move_yline][move_xline] = '▲'
            if  move_xline < xline_num - 1 and area_map[move_yline][move_xline + 1] != '■' and area_map[move_yline][move_xline + 1] != '▲' and area_map[move_yline][move_xline + 1] != '○' :
                area_map[move_yline][move_xline + 1] = '○'
                next_pos.append([move_yline,move_xline + 1])
                pos_g.append(1)
                pos_h.append(abs(end_xline - move_xline - 1)**2 + abs(end_yline - move_yline)**2)
                pos_f.append(1 + abs(end_xline - move_xline - 1)**2 + abs(end_yline - move_yline)**2)
                
            if  area_map[move_yline][move_xline - 1] != '■' and area_map[move_yline][move_xline - 1] != '▲' and area_map[move_yline][move_xline - 1] != '○' and move_xline > 0:
                area_map[move_yline][move_xline - 1] = '○'
                next_pos.append([move_yline,move_xline - 1])
                pos_g.append(1)
                pos_h.append(abs(end_xline - move_xline + 1)**2 + abs(end_yline - move_yline)**2)
                pos_f.append(1 + abs(end_xline - move_xline + 1)**2 + abs(end_yline - move_yline)**2)
                
            if  move_yline < yline_num - 1 and area_map[move_yline + 1][move_xline] != '■' and area_map[move_yline + 1][move_xline] != '▲' and area_map[move_yline + 1][move_xline] != '○':
                area_map[move_yline + 1][move_xline] = '○'
                next_pos.append([move_yline + 1,move_xline])
                pos_g.append(1)
                pos_h.append(abs(end_xline - move_xline)**2 + abs(end_yline - move_yline - 1)**2)
                pos_f.append(1 + abs(end_xline - move_xline)**2 + abs(end_yline - move_yline - 1)**2)
                
            if  area_map[move_yline - 1][move_xline] != '■' and area_map[move_yline - 1][move_xline] != '▲' and area_map[move_yline - 1][move_xline] != '○' and move_yline > 0:
                area_map[move_yline - 1][move_xline] = '○'
                next_pos.append([move_yline - 1,move_xline])
                pos_g.append(1)
                pos_h.append(abs(end_xline - move_xline)**2 + abs(end_yline - move_yline + 1)**2)
                pos_f.append(1 + abs(end_xline - move_xline)**2 + abs(end_yline - move_yline + 1)**2)
                
            if  area_map[move_yline - 1][move_xline - 1] != '■' and area_map[move_yline - 1][move_xline - 1] != '▲' and area_map[move_yline - 1][move_xline - 1] != '○'and move_xline > 0 and move_yline > 0:
                area_map[move_yline - 1][move_xline - 1] = '○'
                next_pos.append([move_yline - 1,move_xline - 1])
                pos_g.append(1.4)
                pos_h.append(abs(end_xline - move_xline + 1)**2 + abs(end_yline - move_yline + 1)**2)
                pos_f.append(1.4 + abs(end_xline - move_xline + 1)**2 + abs(end_yline - move_yline + 1)**2)
                
            if  move_xline < xline_num - 1 and area_map[move_yline - 1][move_xline + 1] != '■' and area_map[move_yline - 1][move_xline + 1] != '▲' and area_map[move_yline - 1][move_xline + 1] != '○' and move_yline > 0:
                area_map[move_yline - 1][move_xline + 1] = '○'
                next_pos.append([move_yline - 1,move_xline + 1])
                pos_g.append(1.4)
                pos_h.append(abs(end_xline - move_xline - 1)**2 + abs(end_yline - move_yline + 1)**2)
                pos_f.append(1.4 + abs(end_xline - move_xline - 1)**2 + abs(end_yline - move_yline + 1)**2)
                
            if  move_yline < yline_num - 1 and area_map[move_yline + 1][move_xline - 1] != '■' and area_map[move_yline + 1][move_xline - 1] != '▲' and area_map[move_yline + 1][move_xline - 1] != '○' and move_xline > 0:
                area_map[move_yline + 1][move_xline - 1] = '○'
                next_pos.append([move_yline + 1,move_xline - 1])
                pos_g.append(1.4)
                pos_h.append(abs(end_xline - move_xline + 1)**2 + abs(end_yline - move_yline - 1)**2)
                pos_f.append(1.4 + abs(end_xline - move_xline + 1)**2 + abs(end_yline - move_yline - 1)**2)
                
            if  move_yline < yline_num - 1 and move_xline < xline_num - 1 and area_map[move_yline + 1][move_xline + 1] != '■' and area_map[move_yline + 1][move_xline + 1] != '▲' and area_map[move_yline + 1][move_xline + 1] != '○':
                area_map[move_yline + 1][move_xline + 1] = '○'
                next_pos.append([move_yline + 1,move_xline + 1])
                pos_g.append(1.4)
                pos_h.append(abs(end_xline - move_xline - 1)**2 + abs(end_yline - move_yline - 1)**2)
                pos_f.append(1.4 + abs(end_xline - move_xline - 1)**2 + abs(end_yline - move_yline - 1)**2)
                
            click_check = 1
        elif click_check == 1:
            for a in range(len(pos_f)):
                move_ready.append(pos_f[a])
            move_ready.sort()
            move_xline = next_pos[pos_f.index(move_ready[0])][1]
            move_yline = next_pos[pos_f.index(move_ready[0])][0]
            area_map[move_yline][move_xline] = '▲'
            pass_pos.append(next_pos[pos_f.index(move_ready[0])])
            next_pos.remove(next_pos[pos_f.index(move_ready[0])])
            pos_g.remove(pos_g[pos_f.index(move_ready[0])])
            pos_h.remove(pos_h[pos_f.index(move_ready[0])])
            pos_f.remove(pos_f[pos_f.index(move_ready[0])])  
            move_ready.clear()
            click_check = 0
        print("next_pos =",next_pos)
        print("pass_pos =",pass_pos)
        print("pos_g    =",pos_g)
        print("pos_h    =",pos_h)
        print("pos_f    =",pos_f)
        if move_xline == end_xline and move_yline == end_yline :
            astar_algorizm_back()
    else:
        astar_algorizm_back()
    display_terminal_map()
    view_pygame_map()
def astar_algorizm_back():
    global end_start, once_check, move_yline, move_xline
    end_start = 1
    area_map[move_yline][move_xline] = 'V'
    print('start_xline = ',start_xline)
    print('start_yline = ',start_yline)
    print('move_xline = ',move_xline)
    print('move_yline = ',move_yline)
    # while move_xline != start_xline and move_yline != start_yline:
    if area_map[move_yline][move_xline+1] == '▲':
        once_check = once_check + 1
    if area_map[move_yline][move_xline-1] == '▲':
        once_check = once_check + 1
    if area_map[move_yline+1][move_xline] == '▲':
        once_check = once_check + 1
    if area_map[move_yline-1][move_xline] == '▲':
        once_check = once_check + 1
    if area_map[move_yline+1][move_xline-1] == '▲':
        once_check = once_check + 1
    if area_map[move_yline+1][move_xline+1] == '▲':
        once_check = once_check + 1
    if area_map[move_yline-1][move_xline-1] == '▲':
        once_check = once_check + 1
    if area_map[move_yline-1][move_xline+1] == '▲':
        once_check = once_check + 1
    if once_check == 1 :
        if area_map[move_yline][move_xline+1] == '▲':
            area_map[move_yline][move_xline+1] = 'V'
            move_xline = move_xline+1
        if area_map[move_yline][move_xline-1] == '▲':
            area_map[move_yline][move_xline-1] = 'V'
            move_xline = move_xline-1
        if area_map[move_yline+1][move_xline] == '▲':
            area_map[move_yline+1][move_xline] = 'V'
            move_yline = move_yline+1
        if area_map[move_yline-1][move_xline] == '▲':
            area_map[move_yline-1][move_xline] = 'V'
            move_yline = move_yline-1
        if area_map[move_yline+1][move_xline-1] == '▲':
            area_map[move_yline+1][move_xline-1] = 'V'
            move_yline = move_yline+1
            move_xline = move_xline-1
        if area_map[move_yline+1][move_xline+1] == '▲':
            area_map[move_yline+1][move_xline+1] = 'V'
            move_yline = move_yline+1
            move_xline = move_xline+1
        if area_map[move_yline-1][move_xline-1] == '▲':
            area_map[move_yline-1][move_xline-1] = 'V'
            move_yline = move_yline-1
            move_xline = move_xline-1
        if area_map[move_yline-1][move_xline+1] == '▲':
            area_map[move_yline-1][move_xline+1] = 'V'
            move_yline = move_yline-1
            move_xline = move_xline+1
    once_check = 0
        
        
## 프로그램 구동
def run_program():
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 게임 화면 종료
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click_help(event)
                if map_click_lock == 0: mouse_click_map(event)
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if (keys[pygame.K_SPACE]):
                    print("K_SPACE 누름")
                    astar_algorizm()
                if (keys[pygame.K_TAB]): 
                    print("K_TAB 누름")
                    tab_click_check()
                if (keys[pygame.K_ESCAPE]):
                    print("K_ESCAPE 누름")
        # if end_start == 1:
        #     astar_algorizm_back()
        view_pygame_map()
        display_area_map()
        clock.tick(30)
        pygame.display.update()
        
run_program()