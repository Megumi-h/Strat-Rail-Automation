import cv2
import numpy as np
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement
import pydirectinput


# 定义节点类
class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.g = 0  # 距离起点的距离
        self.h = 0  # 距离终点的距离
        self.f = 0  # 总花费
        self.parent = None
        self.walkable = True

    def __lt__(self, other):
        return self.f < other.f


# 计算两个节点之间的曼哈顿距离
def manhattan_distance(node1, node2):
    return abs(node1.x - node2.x) + abs(node1.y - node2.y)


# A*算法
def astar(start_node, end_node, grid):
    # 待遍历的节点
    open_set = [start_node]
    # 已遍历的节点
    closed_set = []

    while open_set:
        # 获取当前最佳节点
        current_node = min(open_set)
        # 把当前节点从open_set中删除，放到closed_set里面
        open_set.remove(current_node)
        closed_set.append(current_node)

        # 到达终点，返回路径
        if current_node == end_node:
            path = []
            while current_node:
                path.append((current_node.x, current_node.y))
                current_node = current_node.parent
            path.reverse()
            return path

        # 处理相邻节点
        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            neighbor_x = current_node.x + dx
            neighbor_y = current_node.y + dy

            # 检查相邻节点是否越界或不可通过
            if neighbor_x < 0 or neighbor_x >= grid.width or neighbor_y < 0 or neighbor_y >= grid.height:
                continue

            neighbor_node = grid.nodes[neighbor_y][neighbor_x]
            if not neighbor_node.walkable:
                continue

            # 计算从当前节点到相邻节点的距离
            distance = manhattan_distance(current_node, neighbor_node)

            # 计算相邻节点到终点的估计距离
            h = manhattan_distance(neighbor_node, end_node)

            # 计算总花费
            f = current_node.g + distance + h

            # 如果相邻节点已经被遍历过了，更新总花费和父节点
            if neighbor_node in closed_set:
                if f < neighbor_node.f:
                    neighbor_node.g = current_node.g + distance
                    neighbor_node.h = h
                    neighbor_node.f = f
                    neighbor_node.parent = current_node
            # 否则加入待遍历列表中
            elif neighbor_node in open_set:
                if f < neighbor_node.f:
                    neighbor_node.g = current_node.g + distance
                    neighbor_node.h = h
                    neighbor_node.f = f
                    neighbor_node.parent = current_node
            else:
                neighbor_node.g = current_node.g + distance
                neighbor_node.h = h
                neighbor_node.f = f
                neighbor_node.parent = current_node
                open_set.append(neighbor_node)

    # 没有找到路径
    return None


def simulate_keyboard_directions(path):
    for i in range(18, len(path) - 1, 6):
        current_node = path[i]
        next_node = path[i + 1]
        print(current_node)
        print(next_node)
        if current_node[0] == next_node[0]:
            if current_node[1] > next_node[1]:  # 往上方运动w
                pydirectinput.keyUp('w')
                pydirectinput.keyUp('a')
                pydirectinput.keyUp('d')
                pydirectinput.keyDown('s')
            elif current_node[1] < next_node[1]:  # 往下方运动
                pydirectinput.keyUp('a')
                pydirectinput.keyUp('s')
                pydirectinput.keyUp('d')
                pydirectinput.keyDown('w')
        elif current_node[1] == next_node[1]:
            if current_node[0] > next_node[0]:  # 往左方运动
                pydirectinput.keyUp('w')
                pydirectinput.keyUp('a')
                pydirectinput.keyUp('s')
                pydirectinput.keyDown('d')
            elif current_node[0] < next_node[0]:  # 往右方运动
                pydirectinput.keyUp('w')
                pydirectinput.keyUp('s')
                pydirectinput.keyUp('d')
                pydirectinput.keyDown('a')
        else:  # 对角线运动
            if current_node[0] > next_node[0] and current_node[1] > next_node[1]:  # 向左上方
                pydirectinput.keyUp('w')
                pydirectinput.keyUp('a')
                pydirectinput.keyDown('s')
                pydirectinput.keyDown('d')
            elif current_node[0] > next_node[0] and current_node[1] < next_node[1]:  # 向右上方
                pydirectinput.keyUp('w')
                pydirectinput.keyUp('d')
                pydirectinput.keyDown('s')
                pydirectinput.keyDown('a')
            elif current_node[0] < next_node[0] and current_node[1] > next_node[1]:  # 向左下方
                pydirectinput.keyUp('a')
                pydirectinput.keyUp('s')
                pydirectinput.keyDown('w')
                pydirectinput.keyDown('d')
            elif current_node[0] < next_node[0] and current_node[1] < next_node[1]:  # 向右下方
                pydirectinput.keyUp('s')
                pydirectinput.keyUp('d')
                pydirectinput.keyDown('w')
                pydirectinput.keyDown('a')
    pydirectinput.keyUp('w')
    pydirectinput.keyUp('a')
    pydirectinput.keyUp('s')
    pydirectinput.keyUp('d')


# simulate_keyboard_directions(path)
