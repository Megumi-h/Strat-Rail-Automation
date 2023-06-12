from autogame.Image_judgement import get_game_image, locate_template
import cv2 as cv
import time
import win32gui
import random
import pydirectinput
from pynput import mouse, keyboard

K = keyboard.Controller()


def is_in_map():
    print('开始锄地')
    time.sleep(0.5)
    print("使用过程请勿触碰键盘鼠标，会影响脚本运行.")
    time.sleep(0.5)

    # 查找游戏窗口是否存在
    win_class = 'UnityWndClass'
    win_title = '崩坏：星穹铁道'
    game_win = win32gui.FindWindow(win_class, win_title)
    if game_win == 0:
        print("没有找到崩铁的游戏窗口，请先进入游戏再运行脚本！")
    else:
        print("找到游戏窗口！")
        time.sleep(0.3)

        # 将游戏窗口调前台
        win32gui.SetForegroundWindow(game_win)
        time.sleep(1)

        print('识别是否在地图界面')
        time.sleep(0.3)
        while True:
            # 获取游戏画面
            img, left, top = get_game_image(game_win)
            # 读取模板图片进行匹配
            template_path = './png/map.png'
            map_area = locate_template(img, template_path)
            if map_area is not None:
                print('已在地图界面')
                time.sleep(0.3)
                break
            else:
                print('识别到未在地图界面，开始打开地图')
                time.sleep(0.3)
                # 若未在地图界面就打开地图
                K.press('m')
                K.release('m')
                time.sleep(1.5)
        # 获取游戏画面
        img, left, top = get_game_image(game_win)

        # 圈出识别结果
        cv.rectangle(img, map_area[0], map_area[1], (0, 0, 255), 2)

        # 随机点击范围区域
        x1 = random.randint(map_area[0][0], map_area[1][0])
        y1 = random.randint(map_area[0][1], map_area[1][1])

        x1 += left
        y1 += top

        M = mouse.Controller()
        pydirectinput.mouseDown(x1, y1)
        pydirectinput.mouseUp()
        time.sleep(0.3)
        print('进入星轨航图')
        time.sleep(0.3)
        M.click(mouse.Button.left, 1)
        time.sleep(1)
        print('缩小航图')
        time.sleep(0.2)
        for i in range(6):
            M.scroll(0, -1)
            time.sleep(0.01)
        pydirectinput.mouseDown()
        pydirectinput.mouseUp()
        time.sleep(1.2)
