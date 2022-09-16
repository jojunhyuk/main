import os
from string import capwords
from timeit import repeat
import pygame
import sys
import schedule
import random
import ctypes
import math
import time

os.system("cls")
pygame.init()

# 원카드

dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir)

## 프로그램 실행시 기초 세팅(처음이자 마지막)
def first_setting():
    global done, screen, clock, screensize, user32, time_count, test_count40, count_time
    done = False
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    screen = pygame.display.set_mode(screensize)
    # size = [1070, 700]
    # screen = pygame.display.set_mode(size)
    
    screen.fill([0,0,0])
    clock = pygame.time.Clock()
    time_count = 40
    test_count40 = 0
    count_time = 0

    global img_xsize, img_ysize, card_share_count, reset_button, turn_change, damage_stack, attack_start, before_original_card, start_wait
    img_xsize = 71
    img_ysize = 96
    card_share_count = 10 # 나눠줄 카드 개수
    start_wait = 0
    reset_button = 0
    turn_change = 0
    damage_stack = 1
    attack_start = 0
    before_original_card = 0
    
    global cards_image, background, image2       # 기초 배치 이미지
    background = pygame.transform.scale(pygame.image.load('image/onecard_background_image.jpg'), (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)))
    cards_image = pygame.image.load("image/onecard_image.png")
    image2 = pygame.transform.scale(pygame.image.load('image/onecard.png'), (20, 20))
first_setting()

## 전체 카드를 54개 채우기 / 카드 정렬 배열
def backup_unused_card():
    global unused_cards, unused_cards_num
    unused_cards_num = 54
    unused_cards = []
    unused_cards.clear()
    card_order_number = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
    card_order_shape = ["clover","space","heart","diamond","jorker"]
    card_jorker_color = ["black","color"]
    card_num = 1
    ## 완성된 카드의 형식 [[card_num,image_position,number,shape],......]
    
    ## 54개 카드 분류 card_1 ~ card_54 , 이미지 좌표 ,['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
    for repeat in range(5):
        if repeat != 4:
            for num in range(13):
                unused_cards.append([("card_"+str(card_num)),(img_xsize*num,img_ysize*repeat,img_xsize*1,img_ysize*1)])
                unused_cards[card_num-1].append(card_order_number[num])
                card_num = card_num + 1
        if repeat == 4:
            for num in range(2):
                unused_cards.append([("card_"+str(card_num)),(img_xsize*num,img_ysize*repeat,img_xsize*1,img_ysize*1)])
                unused_cards[card_num-1].append("jorker")
                card_num = card_num + 1
                
    ## ['클로버', '스페이스', '하트', '다이아', '조커'] 분류
    for repeat in range(5):
        if repeat != 4:
            for num in range(0+(repeat*13),13+(repeat*13)):
                unused_cards[num].append(card_order_shape[repeat])
        if repeat == 4:
            for num in range(52,54):
                unused_cards[num].append("jorker")
                unused_cards[num].append(card_jorker_color[num-52])
    
## 1번 플레이어 카드 나누기
def player1_card_share():
    global player1_cards_num, unused_cards_num, unused_cards
    for count in range(card_share_count):
        card_choice = random.choice(unused_cards)
        player1_cards.append(card_choice)
        unused_cards.remove(card_choice)
        player1_cards_num = player1_cards_num + 1
        unused_cards_num = unused_cards_num - 1

## 2번 플레이어 카드 나누기
def player2_card_share():
    global player2_cards_num, unused_cards_num, unused_cards
    for count in range(card_share_count):
        card_choice = random.choice(unused_cards)
        player2_cards.append(card_choice)
        unused_cards.remove(card_choice)
        player2_cards_num = player2_cards_num + 1
        unused_cards_num = unused_cards_num - 1

## 시작시 카드 선택 및 배치
def start_card_view():
    global used_cards, unused_cards, used_cards_num, unused_cards_num
    view_used_card = random.choice(unused_cards)
    unused_cards.remove(view_used_card)
    unused_cards_num = unused_cards_num - 1
    used_cards.append(view_used_card)
    used_cards_num = used_cards_num + 1
    screen.blit(cards_image, (user32.GetSystemMetrics(1) * 3 / 4,(user32.GetSystemMetrics(1) / 2)-48), view_used_card[len(used_cards)])
    
## 사용자1/사용자2 카드 이미지 노출
def player_cards_view():
    ## 플레이어1 카드 나열
    for num in range(player1_cards_num):
        screen.blit(cards_image, (user32.GetSystemMetrics(1)*1/2 + 10*(num+1) + (img_xsize*num),50), player1_cards[num][1])
    ## 플레이어2 카드 나열
    for num in range(player2_cards_num):
        screen.blit(cards_image, (user32.GetSystemMetrics(1)*1/2 + 10*(num+1) + (img_xsize*num),user32.GetSystemMetrics(1) - 146), player2_cards[num][1])
    
## 사용된/사용되지않은 카드 이미지 노출
def used_unused_cards_view():
    ## 사용되지 않은 카드 나열
    card_num = 0
    for ynum in range(math.ceil(unused_cards_num/8)):
        if ynum + 1 == math.ceil(unused_cards_num/8):
            for xnum in range(unused_cards_num-((math.ceil(unused_cards_num/8)-1)*8)):
                screen.blit(cards_image, (user32.GetSystemMetrics(1)*23/20 + 10*(xnum+1) + (img_xsize*xnum),(user32.GetSystemMetrics(1) * 3 / 7) - 212 + (106*ynum)), unused_cards[card_num][1])
                card_num = card_num + 1   
        if ynum + 1 != math.ceil(unused_cards_num/8):
            for xnum in range(8):
                screen.blit(cards_image, (user32.GetSystemMetrics(1)*23/20 + 10*(xnum+1) + (img_xsize*xnum),(user32.GetSystemMetrics(1) * 3 / 7) - 212 + (106*ynum)), unused_cards[card_num][1])
                card_num = card_num + 1  
                 
    ## 사용된 카드 나열
    card_num = 0
    for ynum in range(math.ceil(used_cards_num/8)):
        if ynum + 1 == math.ceil(used_cards_num/8):
            for xnum in range(used_cards_num-((math.ceil(used_cards_num/8)-1)*8)):
                screen.blit(cards_image, (user32.GetSystemMetrics(1)/100 + 10*(xnum+1) + (img_xsize*xnum),(user32.GetSystemMetrics(1) * 3 / 7) - 212 + (106*ynum)), used_cards[card_num][1])
                card_num = card_num + 1
        if ynum + 1 != math.ceil(used_cards_num/8):
            for xnum in range(8):
                screen.blit(cards_image, (user32.GetSystemMetrics(1)/100 + 10*(xnum+1) + (img_xsize*xnum),(user32.GetSystemMetrics(1) * 3 / 7) - 212 + (106*ynum)), used_cards[card_num][1])
                card_num = card_num + 1
                
## 카드 겹치기
def view_cards_overlap():
    for num in range(used_cards_num):
        pygame.draw.rect(screen,[0,0,0] ,((user32.GetSystemMetrics(1) * 3 / 4) - (1*num), (user32.GetSystemMetrics(1) / 2)-48 - (1*num), 71, 96))
        pygame.draw.rect(screen,[0,0,0] ,((user32.GetSystemMetrics(1) * 3 / 4) - (1*num), (user32.GetSystemMetrics(1) / 2)-48 - (1*num), 71, 96),1)
    for num in range(unused_cards_num):
        pygame.draw.rect(screen,[100,100,100] ,((user32.GetSystemMetrics(1) * 8 / 9) - (1*num), (user32.GetSystemMetrics(1) / 2)-48 - (1*num), 71, 96))
        pygame.draw.rect(screen,[0,0,0] ,      ((user32.GetSystemMetrics(1) * 8 / 9) - (1*num), (user32.GetSystemMetrics(1) / 2)-48 - (1*num), 71, 96),1)
            
## 게임 시작 혹은 게임 리셋시 카드 초기화 세팅
def reset_setting():
    screen.fill([30,30,30])
    global used_cards, used_cards_num
    used_cards = []
    used_cards.clear()
    used_cards_num = 0
    global view_cards, view_cards_num
    view_cards = []
    view_cards.clear()
    view_cards_num = 0
    global player1_cards, player1_cards_num
    player1_cards = []
    player1_cards.clear()
    player1_cards_num = 0
    global player2_cards, player2_cards_num
    player2_cards = []
    player2_cards.clear()
    player2_cards_num = 0
    global reset_button, turn_change
    reset_button = 1
    turn_change = 0
    backup_unused_card()
    player1_card_share()
    player2_card_share()
    start_card_view()
    used_unused_cards_view()
    player_cards_view()
    view_cards_overlap()
    player_turn_view()
  
## 터미널에서 나눠진 카드 확인
def print_information():
    print("player1_cards_len : ",len(player1_cards))
    print("player1_cards_num : ", player1_cards_num)
    print("player1_cards     : ",     player1_cards)
    print("player2_cards_len : ",len(player2_cards))
    print("player2_cards_num : ", player2_cards_num)
    print("player2_cards     : ",     player2_cards)
    print("unused_cards_len  : ", len(unused_cards))
    print("unused_cards_num  : ",  unused_cards_num)
    print("unused_cards      : ",      unused_cards)
    print("used_cards_len    : ",   len(used_cards))
    print("used_cards_num    : ",    used_cards_num)
    print("used_cards        : ",        used_cards)

## 선택한 카드가 중앙에 배치
def view_select_card():
    for num in range(used_cards_num):
        screen.blit(cards_image, ((user32.GetSystemMetrics(1) * 3 / 4) - (1*num),(user32.GetSystemMetrics(1) / 2)-48 - (1*num)), used_cards[num][1])
    
## 플레이어의 턴 확인 및 낼수 있는 카드 보이기
def player_turn_view():
    ## 플레이어1 카드 나열
    if turn_change == 0 :
        pick_count = 0
        for num in range(player1_cards_num):
            if (player1_cards[num][2] == used_cards[used_cards_num-1][2] or player1_cards[num][3] == used_cards[used_cards_num-1][3]) or player1_cards[num][3] == "jorker" or used_cards[used_cards_num-1][3] == "jorker":
                pygame.draw.rect(screen,[20,200,255] ,(user32.GetSystemMetrics(1)*1/2 + 10*(num+1) + (img_xsize*num),50, 71, 96),3)
            else :
                pygame.draw.rect(screen,[200,20,20] ,(user32.GetSystemMetrics(1)*1/2 + 10*(num+1) + (img_xsize*num),50, 71, 96),3)
                pick_count = pick_count + 1
        if pick_count == player1_cards_num :
            print("낼카드없음")
    ## 플레이어2 카드 나열
    if turn_change == 1 :
        pick_count = 0
        for num in range(player2_cards_num):
            if (player2_cards[num][2] == used_cards[used_cards_num-1][2] or player2_cards[num][3] == used_cards[used_cards_num-1][3]) or player2_cards[num][3] == "jorker" or used_cards[used_cards_num-1][3] == "jorker":
                pygame.draw.rect(screen,[0,200,255] ,(user32.GetSystemMetrics(1)*1/2 + 10*(num+1) + (img_xsize*num),user32.GetSystemMetrics(1) - 146, 71, 96),3)
            else :
                pygame.draw.rect(screen,[200,20,20] ,(user32.GetSystemMetrics(1)*1/2 + 10*(num+1) + (img_xsize*num),user32.GetSystemMetrics(1) - 146, 71, 96),3)
                pick_count = pick_count + 1
        if pick_count == player2_cards_num :
            print("낼카드없음")

# 2인일시 7장 / 3인이상 5장 나누기
# 원카드 규칙1 (같은 문양 혹은 같은 숫자 + 같은 문양의 연속된 숫자 같이 낼수 있음)

# 원카드 규칙2 (공격카드 및 방어하기)

# 원카드 규칙3 (K/Q/J 의 특수효과)

# 원카드 규칙4 (카드를 가져가야할 상황[수비실패, 낼 카드를가 없을떄, 원카드를 외치지 않았을떄])

# 원카드 규칙5 (중앙의 카드가 0개가 된다면 모인 카드를 맨위 1장 빼고 섞어 뒤집어놓기)

## 플레이어1 카드 내기
def player_card_send():
    global used_cards_num, player1_cards_num, turn_change, before_original_card
    used_cards_num = used_cards_num + 1
    player1_cards_num = player1_cards_num - 1
    turn_change = 1
    before_original_card = 1

## 마우스 클릭시 수정
def mouse_click_cards(event):
    global used_cards_num, used_cards, player1_cards_num, player2_cards_num, turn_change, unused_cards_num, unused_cards, damage_stack, attack_start, before_original_card
    row_index         = event.pos[0]
    column_index      = event.pos[1]
    x_line_click = user32.GetSystemMetrics(1)*1/2 
    y_line_click = user32.GetSystemMetrics(1) - 146
    screen.fill([30,30,30])
    
    ## 공격 카드 데미지 누적
    if (used_cards[used_cards_num-1][2] == '2' or used_cards[used_cards_num-1][2] == 'A' or used_cards[used_cards_num-1][2] == 'jorker') and before_original_card == 1:
        attack_start = 1
    if attack_start == 1:
        if used_cards[used_cards_num-1][2] == '2':                                                                damage_stack = damage_stack + 1
        elif used_cards[used_cards_num-1][2] == 'A'      and used_cards[used_cards_num-1][3] != "space":          damage_stack = damage_stack + 2
        elif used_cards[used_cards_num-1][2] == 'A'      and used_cards[used_cards_num-1][3] == "space":          damage_stack = damage_stack + 3
        elif used_cards[used_cards_num-1][2] == 'jorker' and used_cards[used_cards_num-1][4] == 'black' :         damage_stack = damage_stack + 7
        elif used_cards[used_cards_num-1][2] == 'jorker' and used_cards[used_cards_num-1][4] == 'color' :         damage_stack = damage_stack + 9
        else                                                                                            :         damage_stack = damage_stack
    
    ## 플레이어1의 클릭
    if turn_change == 0 :
        if (row_index >= (user32.GetSystemMetrics(1) * 8 / 9) - (1*unused_cards_num) and row_index <= (user32.GetSystemMetrics(1) * 8 / 9) - (1*unused_cards_num) + 72) and (column_index >= (user32.GetSystemMetrics(1) / 2)-48 - (1*unused_cards_num) and column_index <= (user32.GetSystemMetrics(1) / 2)-48 - (1*unused_cards_num) + 96):
            if damage_stack > 1 : attack_start = 0
            for _ in range(damage_stack):
                random_card = random.choice(unused_cards)
                player1_cards.append(random_card)
                player1_cards_num = player1_cards_num + 1
                unused_cards.remove(random_card)
                unused_cards_num = unused_cards_num - 1
            damage_stack = 1
            turn_change = 1
            before_original_card = 0
        for num in range(player1_cards_num):
            if (row_index >= x_line_click + 10*(num+1) + (img_xsize*num)) and row_index <= x_line_click + 10*(num+1) + (img_xsize*(num+1)) and (column_index >= 50 and column_index <= 146) :
                if used_cards[used_cards_num-1][2] == '2' and (player1_cards[num][2] == '2' or (player1_cards[num][2] == 'A' and (player1_cards[num][3] == used_cards[used_cards_num-1][3])) or player1_cards[num][3] == "jorker") :
                    used_cards.append(player1_cards[num])
                    player1_cards.remove(player1_cards[num])
                    player_card_send()
                elif used_cards[used_cards_num-1][2] == 'A' and (player1_cards[num][2] == 'A' or player1_cards[num][3] == "jorker"):
                    used_cards.append(player1_cards[num])
                    player1_cards.remove(player1_cards[num])
                    player_card_send()
                elif used_cards[used_cards_num-1][3] == 'jorker':
                    used_cards.append(player1_cards[num])
                    player1_cards.remove(player1_cards[num])
                    player_card_send()
                else :
                    used_cards.append(player1_cards[num])
                    player1_cards.remove(player1_cards[num])
                    player_card_send()
            
    ## 플레이어2의 클릭
    elif turn_change == 1 :
        if (row_index >= (user32.GetSystemMetrics(1) * 8 / 9) - (1*unused_cards_num) and row_index <= (user32.GetSystemMetrics(1) * 8 / 9) - (1*unused_cards_num) + 72) and (column_index >= (user32.GetSystemMetrics(1) / 2)-48 - (1*unused_cards_num) and column_index <= (user32.GetSystemMetrics(1) / 2)-48 - (1*unused_cards_num) + 96):
            if damage_stack > 1 : attack_start = 0
            for _ in range(damage_stack): 
                random_card = random.choice(unused_cards)
                player2_cards.append(random_card)
                player2_cards_num = player2_cards_num + 1
                unused_cards.remove(random_card)
                unused_cards_num = unused_cards_num - 1
            damage_stack = 1
            turn_change = 0
            before_original_card = 0
        for num in range(player2_cards_num):
            if (row_index >= x_line_click + 10*(num+1) + (img_xsize*num)) and row_index <= x_line_click + 10*(num+1) + (img_xsize*(num+1)) and (column_index >= y_line_click and column_index <= y_line_click + 96) :
                if (player2_cards[num][2] == used_cards[used_cards_num-1][2] or player2_cards[num][3] == used_cards[used_cards_num-1][3]) or player2_cards[num][3] == "jorker" or used_cards[used_cards_num-1][3] == "jorker":
                    used_cards.append(player2_cards[num])
                    used_cards_num = used_cards_num + 1
                    player2_cards_num = player2_cards_num - 1
                    player2_cards.remove(player2_cards[num])
                    turn_change = 0
                    before_original_card = 1

    view_cards_overlap()
    view_select_card()
    player_cards_view()
    used_unused_cards_view()
    player_turn_view()
    
def test_1Sec():
    global test_count40, count_time
    test_count40 += 1
    # print(f"{test_count5}")
    if test_count40 == time_count: 
        test_count40 = 0
        count_time = count_time + 1
    return test_count40
schedule.every(10).seconds.do(test_1Sec)
     
## 게임 종료 선언
def run_close():
    # print_information()
    pygame.quit()
    sys.exit()
    
## 게임 시작 선언
def run_start():
    global start_wait
    screen.blit(background,(0,0))
    start_wait = 1
    
## 게임 시작
def run_program():
    while not done:
        global reset_button
        # os.system("cls")
        for event in pygame.event.get():
            if event.type == pygame.QUIT: run_close() # 게임 화면 종료
            if event.type == pygame.MOUSEBUTTONDOWN: mouse_click_cards(event)
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if (keys[pygame.K_SPACE])  : print("K_SPACE 누름")
                if (keys[pygame.K_TAB])    : reset_button = 0
                if (keys[pygame.K_ESCAPE]) : run_close()
                if (keys[pygame.K_LEFT])   : print("K_LEFT 누름")
                if (keys[pygame.K_RIGHT])  : print("K_RIGHT 누름")
                if (keys[pygame.K_UP])     : print("K_UP 누름")
                if (keys[pygame.K_DOWN])   : print("K_DOWN 누름")
        
        if start_wait == 0                                           : run_start()
        if start_wait == 1 and count_time >= 2 and reset_button == 0 : reset_setting() 
        
        # print_information()
        test_1Sec()
        clock.tick(30)
        schedule.run_pending()
        pygame.display.update()
        
run_program()

