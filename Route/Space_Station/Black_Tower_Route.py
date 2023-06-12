from autogame.Image_judgement import get_game_image, locate_template, Multi_positioning_templates, judgement_scaling, \
    observation_carriage, tp, combat_judgement, access_map_check
import cv2 as cv
import time
import win32api
import win32con
import win32gui
import random
from pynput import mouse, keyboard
import pydirectinput
import sys

M = mouse.Controller()
K = keyboard.Controller()


def planet1():  # 进入空间站「黑塔」
    win_class = 'UnityWndClass'
    win_title = '崩坏：星穹铁道'
    game_win = win32gui.FindWindow(win_class, win_title)
    print("识别开始空间站「黑塔」")
    time.sleep(0.3)
    while True:
        # 获取游戏画面
        img, left, top = get_game_image(game_win)
        # 读取模板图片进行匹配
        template_path = './png/Space_station.png'
        map_area = locate_template(img, template_path)
        if map_area is not None:
            print('找到空间站「黑塔」')
            time.sleep(0.3)
            break
        else:
            print("未识别到空间站「黑塔」，呃呃，请以管理方式重新运行试试")
            time.sleep(2)
            sys.exit()

    # 获取游戏画面
    img, left, top = get_game_image(game_win)
    # 圈出识别结果
    cv.rectangle(img, map_area[0], map_area[1], (0, 0, 255), 2)
    # 随机点击范围区域
    x1 = random.randint(map_area[0][0], map_area[1][0])
    y1 = random.randint(map_area[0][1], map_area[1][1])

    x1 += left
    y1 += top

    M.position = (x1, y1)
    time.sleep(0.3)
    print("开始进入空间站「黑塔」")
    time.sleep(0.3)
    pydirectinput.mouseDown()
    pydirectinput.mouseUp()
    time.sleep(2)


def space_station():  # 基座舱段路线
    win_class = 'UnityWndClass'
    win_title = '崩坏：星穹铁道'
    game_win = win32gui.FindWindow(win_class, win_title)
    #  识别观景车厢然后点击
    observation_carriage(game_win)

    print("开始识别基座舱段")
    time.sleep(0.5)
    while True:
        # 获取游戏画面
        img, left, top = get_game_image(game_win)
        # 读取模板图片进行匹配
        template_path = './png/Base_Compartment.png'
        map_area = locate_template(img, template_path)
        if map_area is not None:
            print('找到基座舱段')
            time.sleep(0.5)
            break
        else:
            print("未识别到基座舱段，呃呃，请以管理方式重新运行试试")
            time.sleep(2)
            sys.exit()
    # 获取游戏画面
    img, left, top = get_game_image(game_win)
    # 圈出识别结果
    cv.rectangle(img, map_area[0], map_area[1], (0, 0, 255), 2)
    # 随机点击范围区域
    x1 = random.randint(map_area[0][0], map_area[1][0])
    y1 = random.randint(map_area[0][1], map_area[1][1])

    x1 += left
    y1 += top

    M.position = (x1, y1)
    print("进入基座舱段地图")
    time.sleep(0.5)
    pydirectinput.mouseDown()
    pydirectinput.mouseUp()
    time.sleep(1)

    # 检查缩放
    judgement_scaling(game_win)

    while True:
        # 获取游戏画面
        img, left, top = get_game_image(game_win)
        print("开始识别锚点")
        time.sleep(0.5)

        template_paths = list()
        template_path1 = cv.imread('./png/Anchor_Points.png')
        template_path2 = cv.imread('./png/Stagnant_Void.png')
        template_paths.append(template_path1)
        template_paths.append(template_path2)
        loc = list()
        for t in template_paths:
            loc += Multi_positioning_templates(img, t)
        if len(loc) > 0:
            print("找到锚点")
            time.sleep(0.5)
            break
        else:
            print("未找到锚点，呃呃，请以管理方式重新运行试试")

    # 圈出识别结果
    for i in loc:
        cv.rectangle(img, (i[0], i[1]), (i[2], i[3]), (0, 255, 0), 2)
    # 随机点击范围区域
    x1 = random.randint(loc[0][0], loc[0][2])
    y1 = random.randint(loc[0][1], loc[0][3])
    x1 += left
    y1 += top

    M.position = (x1, y1)
    time.sleep(0.2)
    M.click(mouse.Button.left, 1)
    time.sleep(0.3)
    tp(game_win)

    # 开始跑路线辣
    numa = 0
    numb = 0
    time.sleep(2)
    access_map_check(game_win)
    for i in range(26):
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 100, 0)
        time.sleep(0.01)
    while True:
        # 获取游戏画面
        img, left, top = get_game_image(game_win)
        # 读取模板图片进行匹配
        template_path = './png/Reference.bmp'
        map_area = locate_template(img, template_path)
        if map_area is not None:
            print('找到参照物')
            time.sleep(0.5)
            break
        else:
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 10, 0)

    numa += 1
    print(f"干翻第{numa}只怪")  # 第1只怪
    time.sleep(0.5)
    K.press('w')
    time.sleep(0.5)
    K.press(keyboard.Key.shift_l)
    time.sleep(0.5)
    K.release(keyboard.Key.shift_l)
    time.sleep(0.5)
    M.click(mouse.Button.left, 1)
    combat_judgement(game_win)

    numb += 1
    print(f"干翻第{numb}个垃圾桶")  # 第1个垃圾桶
    K.press('w')
    time.sleep(0.5)
    K.press(keyboard.Key.shift_l)
    time.sleep(0.5)
    K.release(keyboard.Key.shift_l)
    K.release('w')
    M.click(mouse.Button.left, 1)
    time.sleep(0.5)

    numb += 1
    print(f"干翻第{numb}个垃圾桶")  # 第2个垃圾桶
    K.press('w')
    time.sleep(0.5)
    K.press(keyboard.Key.shift_l)
    time.sleep(0.6)
    K.release(keyboard.Key.shift_l)
    K.press('a')
    time.sleep(0.8)
    K.release('a')
    K.release('w')
    K.press('a')
    time.sleep(1)
    K.release('a')
    time.sleep(1)
    M.click(mouse.Button.left, 1)

    numb += 1
    print(f"干翻第{numb}个垃圾桶")
    time.sleep(0.5)
    K.press('d')
    time.sleep(0.5)
    K.press(keyboard.Key.shift_l)
    time.sleep(0.5)
    K.release(keyboard.Key.shift_l)
    time.sleep(1.2)
    K.release('d')
    K.press('w')
    time.sleep(0.8)
    K.press('d')
    time.sleep(1)
    K.release('d')
    K.release('w')
    M.click(mouse.Button.left, 1)

    numb += 1
    print(f"干翻第{numb}个垃圾桶")
    time.sleep(0.5)
    K.press('w')
    K.press('d')
    time.sleep(0.5)
    K.press(keyboard.Key.shift_l)
    time.sleep(1.2)
    K.release(keyboard.Key.shift_l)
    K.release('d')
    time.sleep(0.7)
    K.release('w')
    M.click(mouse.Button.left, 1)
