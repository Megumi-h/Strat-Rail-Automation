import heapq


# 定义节点类
class Node:
    def __init__(self, x, y, map_data, passable=True):
        self.x = x
        self.y = y
        self.passable = passable and (0 <= y < len(map_data)) and (0 <= x < len(map_data[0])) and map_data[y][x] == 0
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = None

    # 计算节点的哈希值
    def __hash__(self):
        return hash((self.x, self.y, self.passable))

    # 用于在优先级队列中排序节点
    def __lt__(self, other):
        return self.f < other.f

    # 两个节点是否相等
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.passable == other.passable

    def __repr__(self):
        return f"Node({self.x}, {self.y}, {self.passable})"


# A*算法实现
def astar(start_x, start_y, end_x, end_y, map_data):
    # 检查起点和终点是否越界
    if not (0 <= start_x < len(map_data[0]) and 0 <= start_y < len(map_data)):
        raise ValueError("起点坐标越界")
    if not (0 <= end_x < len(map_data[0]) and 0 <= end_y < len(map_data)):
        raise ValueError("终点坐标越界")

    # 初始化起点和终点节点
    start_node = Node(start_x, start_y, map_data)
    end_node = Node(end_x, end_y, map_data)

    # 将起点作为开启列表中的第一个节点
    open_list = []
    heapq.heappush(open_list, start_node)

    # 初始化关闭列表
    closed_list = set()

    # 直到找到终点或开启列表为空
    while open_list:
        # 在开启列表中找出 f 值最小的节点
        current_node = heapq.heappop(open_list)

        # 将该节点加入关闭列表
        closed_list.add(current_node)

        # 当前节点为终点，路径生成完毕，返回路径列表
        if current_node == end_node:
            path = []
            while current_node != start_node:
                path.append((current_node.x, current_node.y))
                current_node = current_node.parent
            path.append((start_node.x, start_node.y))
            return path[::-1]

        # 遍历当前节点的邻居节点
        for i, j in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            neighbour_x = current_node.x + i
            neighbour_y = current_node.y + j

            # 检查邻居节点是否越界
            if not (0 <= neighbour_x < len(map_data[0]) and 0 <= neighbour_y < len(map_data)):
                continue

            neighbour_node = Node(neighbour_x, neighbour_y, map_data)

            # 如果邻居节点不可通过或已在关闭列表中，跳过
            if not neighbour_node.passable or neighbour_node in closed_list:
                continue

            # 更新 g 值、h 值和 f 值
            neighbour_node.g = current_node.g + 1
            neighbour_node.h = (end_node.x - neighbour_node.x) ** 2 + \
                               (end_node.y - neighbour_node.y) ** 2
            neighbour_node.f = neighbour_node.g + neighbour_node.h

            # 如果邻居节点已经在开启列表中，比较新的 f 值和旧的 f 值大小，选择更新
            found_in_open_list = False
            for open_node in open_list:
                if open_node == neighbour_node and neighbour_node.f < open_node.f:
                    heapq.heappush(open_list, neighbour_node)
                    found_in_open_list = True
                    break
            if not found_in_open_list:  # 如果邻居节点不在开启列表中，添加进去
                neighbour_node.parent = current_node
                heapq.heappush(open_list, neighbour_node)

    # 开启列表为空，没有到达终点的路径，返回空列表
    return []


# 地图数据示例
# 0 表示通路，1 表示障碍物
map_data = [[0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0]]

# 起点和终点坐标
start_x, start_y = 0, 0
end_x, end_y = 5, 4

# 寻路并输出路径
path = astar(start_x, start_y, end_x, end_y, map_data)
print(path)
