import math
import random
import time
import matplotlib.pyplot as plt

time_start = time.time()

# 计算两个点之间的欧几里得距离
def euclidean_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# 为城市创建距离矩阵
def create_distance_matrix(cities):
    n = len(cities)
    distance_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            distance_matrix[i][j] = euclidean_distance(cities[i], cities[j])
    return distance_matrix

# 执行3-opt交换
def three_opt_swap(route, i, j, k):
    new_routes = []
    new_routes.append(route[:i] + route[i:j][::-1] + route[j:k][::-1] + route[k:])  # Case 1 此操作将路线中索引 i 到 j 的部分和索引 j 到 k 的部分分别反转，然后重新组合成新路线
    new_routes.append(route[:i] + route[j:k] + route[i:j] + route[k:])  # Case 2 此操作将路线中索引 i 到 j 的部分和索引 j 到 k 的部分交换位置，然后重新组合成新路线
    new_routes.append(route[:i] + route[j:k][::-1] + route[i:j] + route[k:])  # Case 3 此操作将路线中索引 j 到 k 的部分反转，然后将其与索引 i 到 j 的部分交换位置，最后重新组合成新路线
    new_routes.append(route[:i] + route[i:j] + route[j:k][::-1] + route[k:])  # Case 4 此操作仅将路线中索引 j 到 k 的部分反转，然后重新组合成新路线
    new_routes.append(route[:i] + route[j:k] + route[i:j][::-1] + route[k:])  # Case 5 此操作仅将路线中索引 i 到 j 的部分反转，然后重新组合成新路线
    new_routes.append(route[:i] + route[i:j][::-1] + route[j:k] + route[k:])  # Case 6 此操作将路线中索引 i 到 j 的部分反转，然后重新组合成新路线
    return new_routes

# 计算路线的总距离
def calculate_total_distance(route, distance_matrix):
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += distance_matrix[route[i]][route[i + 1]]
    total_distance += distance_matrix[route[-1]][route[0]]  # 返回起始城市
    return total_distance

# LKH 算法
def lkh_algorithm(cities):
    distance_matrix = create_distance_matrix(cities)
    n = len(cities)
    best_route = list(range(n))
    # 使用贪心算法生成初始解
    #unvisited = set(range(n))
    #current_city = random.choice(list(unvisited))
    #unvisited.remove(current_city)
    #best_route = [current_city]

    #while unvisited:
    #    next_city = min(unvisited, key=lambda city: distance_matrix[current_city][city])
    #    unvisited.remove(next_city)
    #    best_route.append(next_city)
    #    current_city = next_city


    # 使用随机算法生成初始解
    #random.shuffle(best_route)

    best_distance = calculate_total_distance(best_route, distance_matrix)
    
    improvement = True
    tried_combinations = set()  # 用于记录已经尝试过的边组合，避免重复尝试
    while improvement:
        improvement = False
        for i in range(n - 2):
            for j in range(i + 1, n - 1):
                for k in range(j + 1, n):
                    combination = (i, j, k)
                    if combination in tried_combinations:
                        continue
                    tried_combinations.add(combination)
                    new_routes = three_opt_swap(best_route, i, j, k)
                    for new_route in new_routes:
                        new_distance = calculate_total_distance(new_route, distance_matrix)
                        if new_distance < best_distance:
                            best_route = new_route
                            best_distance = new_distance
                            improvement = True
                            break
                    if improvement:
                        break
                if improvement:
                    break
            if improvement:
                break
    
    return best_route, best_distance

# 城市列表
cities = [
    (22, 22), (36, 26), (21, 45), (45, 35), (55, 20), (33, 34), (50, 50), (55, 45), (26, 59), (40, 66),
    (55, 65), (35, 51), (62, 35), (62, 57), (62, 24), (21, 36), (33, 44), (9, 56), (62, 48), (66, 14),
    (44, 13), (26, 13), (11, 28), (7, 43), (17, 64), (41, 46), (55, 34), (35, 16), (52, 26), (43, 26),
    (31, 76), (22, 53), (26, 29), (50, 40), (55, 50), (54, 10), (60, 15), (47, 66), (30, 60), (30, 50),
    (12, 17), (15, 14), (16, 19), (21, 48), (50, 30), (51, 42), (50, 15), (48, 21), (12, 38), (15, 56),
    (29, 39), (54, 38), (55, 57), (67, 41), (10, 70), (6, 25), (65, 27), (40, 60), (70, 64), (64, 4),
    (36, 6), (30, 20), (20, 30), (15, 5), (50, 70), (57, 72), (45, 42), (38, 33), (50, 4), (66, 8),
    (59, 5), (35, 60), (27, 24), (40, 20), (40, 37), (40, 40)
]

# 使用LKH算法解决TSP问题
best_route, best_distance = lkh_algorithm(cities)
best_route.append(best_route[0]) # 算法给出的路径并未包括起点，添加回到起点的路径
# best_distance += euclidean_distance(cities[best_route[-2]], cities[best_route[-1]])
# 展示时有失误，最后一个城市和第一个城市的距离重复进行计算，导致最终结果偏长
print(best_route[-1], best_route[-2])
print(euclidean_distance(cities[best_route[-2]], cities[best_route[-1]]))
print("最佳路线:", best_route)
print("最佳距离:", best_distance)
time_end = time.time()
print('Time cost:', (time_end - time_start) * 1000, 'ms')