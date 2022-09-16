from re import I
import os

from pynput import keyboard

os.system("cls")

dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir)







use_map =[]
######################################################### 기본 맵, 나열 맵, x축, y축 출력 map_open()
def map_open():
    map_txt = open('txt/maze.txt', 'r', encoding='utf-8')
    global x_line, y_line, trans_map, origin_map
    origin_map = map_txt.read()
    x_line = origin_map.replace(' ','').find('\n')
    y_line = int(len(origin_map.replace(' ','').replace('\n',''))/x_line)
    trans_map = origin_map.replace(' ','').replace('\n','')
    map_txt.close()
map_open()
######################################################### 배열 맵 출력 map_clear()
def map_clear():
    map_txt = open('txt/maze.txt', 'r', encoding='utf-8')
    while True:
        line_map = map_txt.readline()
        if not line_map:
            break
        line_map = line_map.replace('\n','')
        clear_map = line_map.split(' ')
        use_map.append(clear_map)
    map_txt.close()
map_clear()
######################################################### 맵 위치 x축 y축 변경(왼쪽 아래를 0,0으로)하여 x축 y축 값 출력 change_pos(x,y)
def change_pos(x,y):
    
    row = x
    col = y_line - (y + 1)

    return(col,row)
######################################################### 맵 위치 x축 y축 변경(왼쪽 아래를 0,0으로)하여 자리값 출력 position(x,y)
def position(x,y):

    row = x
    col = y_line - (y + 1)

    print(use_map[col][row])
######################################################### 나열 맵에서 나온 위치값을 x,y 형식을 바꿔줌 share_xy(num)
def share_xy(num):
    
    num_y = num // x_line
    num_x = num % x_line

    return num_x,num_y
######################################################### x,y 형식을 나열 맵에서 나온 위치값으로 바꿔줌 share_num(x,y)
def share_num(x,y):
    
    num = x + (y * x_line)

    return num
######################################################### 고정정보 입력
start_num = trans_map.find('s')
finish_num = trans_map.find('f')
player_num = start_num
######################################################### 변동정보 입력
player_x = share_xy(player_num)[0]
player_y = share_xy(player_num)[1]
######################################################### 변경되는 맵 생성
def change_map():
    for y in range(0,y_line):
        for x in range(0,x_line):
            
            if(player_y == y and player_x == x): 
                print('▲', end = ' ')
            else:
                print(use_map[y][x], end = ' ')
        print()
######################################################### 키보드에 입력값이 생길때
key_press = 0
move_count = 0
comment = '김밥 편의점 탈출 강행'
def on_press(key):
    global player_y, player_x, key_press, comment, move_count
    try:
        print('alphanumeric key {0} pressed'.format(key.char))
    except AttributeError:
        if key == keyboard.Key.up       : 
            # print('위쪽')
            if use_map[player_y - 1][player_x] == 'x' : comment = '그 방향은 막혀있다'
            else :
                player_y = player_y - 1
                comment = '삼각김밥이 위로 이동함'
                move_count += 1
        if key == keyboard.Key.down     : 
            # print('아래')
            if use_map[player_y + 1][player_x] == 'x' : comment = '그 방향은 막혀있다'
            else :
                player_y = player_y + 1
                comment = '삼각김밥이 아래로 이동함'
                move_count += 1
        if key == keyboard.Key.left     : 
            # print('왼쪽')
            if use_map[player_y][player_x - 1] == 'x' : comment = '그 방향은 막혀있다'
            else :
                player_x = player_x - 1
                comment = '삼각김밥이 왼쪽으로 이동함'
                move_count += 1
        if key == keyboard.Key.right    : 
            # print('오른쪽')
            if use_map[player_y][player_x + 1] == 'x' : comment = '그 방향은 막혀있다'
            else :
                player_x = player_x + 1
                comment = '삼각김밥이 오른쪽으로 이동함'
                move_count += 1
        # print('{0} pressed'.format(key))
        key_press = 1
######################################################### 키보드에서 입력이 멈출때
def on_release(key):
    # print('{0} released'.format(
    #     key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

######################################################### 키보드 모니터링
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

######################################################### 실행
while True:

    if change_pos(player_x,player_y) == change_pos(share_xy(finish_num)[0],share_xy(finish_num)[1]):
        break
    key_press = 0
    print("<< 삼각김밥 편의점 탈출 >>")
    change_map()
    print(f"\n시작위치 : {change_pos(share_xy(start_num)[0],share_xy(start_num)[1])}")
    print(f"도착위치 : {change_pos(share_xy(finish_num)[0],share_xy(finish_num)[1])}")
    print(f"삼각김밥 위치 : {change_pos(player_x,player_y)} \n")
    print(f"움직인 횟수 : {move_count}")
    print(f"상황 : {comment}")

    while key_press == 0:
        if key_press == 1 : break

    os.system("cls")
######################################################### 종료
def ending():
    print(" <<< 지도 맵 >>> ")
    change_map()
    print(f"\n시작위치 : {change_pos(share_xy(start_num)[0],share_xy(start_num)[1])}")
    print(f"도착위치 : {change_pos(share_xy(finish_num)[0],share_xy(finish_num)[1])}")
    print(f"플레이어 위치 : {change_pos(player_x,player_y)} \n")
    print(f"움직인 횟수 : {move_count}")
    print("상황 : 삼각김밥은 편의점을 탈출해 행복하게 오래오래 살았다.")
ending()


