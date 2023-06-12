import sys
import cv2 as cv
import numpy as np
import win32gui
import time
import random
from PIL import ImageGrab
from pynput import mouse, keyboard
M = mouse.Controller()
K = keyboard.Controller()


def get_game_image(game_win):  # 获取游戏窗口画面
    # 获取游戏窗口左上到右下两角的坐标
    left, top, _, _ = win32gui.GetWindowRect(game_win)
    _, _, width, height = win32gui.GetClientRect(game_win)

    # 指定区域为游戏内容区域
    left += 8
    top += 31
    right = width + left
    bottom = height + top

    # 截取游戏画面并缓存
    img = np.array(ImageGrab.grab(bbox=(left, top, right, bottom)))  # type: ignore
    _, buffer = cv.imencode('game_screenshot.png', img)

    # 从内存缓存中读取图像
    img = cv.imdecode(buffer, cv.IMREAD_GRAYSCALE)

    return img, left, top


def locate_template(img, template_gray):  # 单模版匹配
    template = cv.imread(template_gray)
    template_gray = cv.cvtColor(template, cv.COLOR_BGR2GRAY)
    height, width = template_gray.shape
    result = cv.matchTemplate(img, template_gray, cv.TM_CCOEFF_NORMED)
    minValue, maxValue, minLoc, maxLoc = cv.minMaxLoc(result)

    if maxValue < 0.9:
        return None

    left_top = maxLoc
    right_bottom = (maxLoc[0] + width, maxLoc[1] + height)
    cv.rectangle(img, left_top, right_bottom, (0, 255, 0), 2)

    # cv.imshow('img', img)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    return left_top, right_bottom


def Multi_positioning_templates(img, template_path):  # 多模版匹配多目标
    template_gray = cv.cvtColor(template_path, cv.COLOR_BGR2GRAY)
    height, width = template_gray.shape
    res = cv.matchTemplate(img, template_gray, cv.TM_CCOEFF_NORMED)
    matches = 0.8  # 匹配度
    loc = np.where(res >= matches)  # 把符合要求的传入loc变量
    loc_all = list()  # 创建loc_all列表
    for left, top in zip(*loc[::-1]):  # 倒序重组把匹配的坐标导入left, top
        loc_all.append((left, top, left + width, top + height))  # 计算出左上右下坐标
    if len(loc_all) == 0:
        return []

    return loc_all


def observation_carriage(game_win):
    while True:
        # 获取游戏画面
        img, left, top = get_game_image(game_win)
        # 读取模板图片进行匹配
        template_path = './png/Observation_Carriage.bmp'
        map_area = locate_template(img, template_path)
        if map_area is not None:
            # 随机点击范围区域
            x1 = random.randint(map_area[0][0], map_area[1][0])
            y1 = random.randint(map_area[0][1], map_area[1][1])
            x1 += left
            y1 += top
            M.position = (x1, y1)
            time.sleep(0.1)
            M.click(mouse.Button.left, 1)
        else:
            break


def judgement_scaling(game_win):
    while True:
        # 获取游戏画面
        img, left, top = get_game_image(game_win)
        template_path = './png/Scaling.bmp'
        map_area = locate_template(img, template_path)
        print("识别地图是否缩放到最小")
        if map_area is not None:
            print("已缩放至最小")
            time.sleep(0.5)
            break
        else:
            print("没有缩放至最小，开始缩放")
            time.sleep(0.5)
            # 获取左上坐标和游戏画面宽高
            _, _, width, height = win32gui.GetClientRect(game_win)
            # 去掉标题栏的左上坐标
            left += 8
            top += 31

            half_width = width/2
            half_height = height/2

            center = (left + half_width, top + half_height)
            time.sleep(0.5)
            M.position = center
            time.sleep(2)
            time.sleep(0.5)
            for i in range(10):
                M.scroll(0, -1)
                time.sleep(0.01)
            time.sleep(1.5)


def tp(game_win):
    while True:
        # 获取游戏画面
        img, left, top = get_game_image(game_win)
        template_path = './png/tp.bmp'
        map_area = locate_template(img, template_path)
        if map_area is not None:
            print("识别到传送按钮")
            time.sleep(0.3)
            # 获取游戏画面
            img, left, top = get_game_image(game_win)
            # 圈出识别结果
            cv.rectangle(img, map_area[0], map_area[1], (0, 0, 255), 2)
            # 随机点击范围区域
            print("TP！XD")
            x1 = random.randint(map_area[0][0], map_area[1][0])
            y1 = random.randint(map_area[0][1], map_area[1][1])
            x1 += left
            y1 += top
            M.position = (x1, y1)
            M.click(mouse.Button.left, 1)
            break
        else:
            print("未识别传送按钮，呃呃，请以管理方式重新运行试试")
            sys.exit()


def combat_judgement(game_win):
    i = 0
    while True:
        # 获取游戏画面
        img, left, top = get_game_image(game_win)
        template_path = './png/Suspension.bmp'
        map_area = locate_template(img, template_path)
        if map_area is not None:
            K.release('w')
            print("战斗中...  等待战斗结束")
            time.sleep(2)
            break
        else:
            if i < 2:
                time.sleep(1.25)
                M.click(mouse.Button.left, 1)
                i += 1
            else:
                break
    while True:
        # 获取游戏画面
        img, left, top = get_game_image(game_win)
        template_path = './png/phone.bmp'
        map_area = locate_template(img, template_path)
        if i == 2:
            K.release('w')
            print("没怪了辣，执行下一个地点")
            time.sleep(0.5)
            break
        if map_area is None:
            print("战斗结束")
            time.sleep(2)
            break


def access_map_check(game_win):
    while True:
        # 获取游戏画面
        img, left, top = get_game_image(game_win)
        # 读取模板图片进行匹配
        template_paths = list()
        template_path1 = cv.imread('./png/phone.bmp')
        template_path2 = cv.imread('./png/phone1.bmp')
        template_paths.append(template_path1)
        template_paths.append(template_path2)
        loc = list()
        for t in template_paths:
            loc += Multi_positioning_templates(img, t)
        if len(loc) > 0:
            print("进图成功")
            time.sleep(0.5)
            break
