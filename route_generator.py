# Description: This file contains the implementation of the route generator algorithm.

'''File Contains:
    1. euclidean_distance function: This function is used to calculate the Euclidean distance between two coordinates.
    2. construct_mst function: This function is used to construct the Minimum Spanning Tree (MST) of the given coordinates.
    3. dfs_traversal function: This function is used to perform Depth First Search (DFS) traversal on the MST.
    4. generate_route function: This function is used to generate the route based on the DFS traversal.
    5. calculate_total_distance function: This function is used to calculate the total distance of the generated route.'''

# Importing required libraries
import math
from typing import List, Tuple
from heapq import heappop, heappush


# euclidean_distance function is used to calculate the Euclidean distance between two coordinates
def euclidean_distance(coord1: Tuple[int, int], coord2: Tuple[int, int]) -> float:
    return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)


# construct_mst function is used to construct the Minimum Spanning Tree (MST) of the given coordinates
def construct_mst(coordinates: List[Tuple[int, int]]) -> List[List[int]]:
    n = len(coordinates)
    adj_list = [[] for _ in range(n)]
    visited = [False] * n
    min_heap = [(0, 0, -1)]

    while min_heap:
        weight, current, parent = heappop(min_heap)
        if visited[current]:
            continue
        visited[current] = True
        if parent != -1:
            adj_list[parent].append(current)
            adj_list[current].append(parent)

        for next_node in range(n):
            if not visited[next_node]:
                dist = euclidean_distance(coordinates[current], coordinates[next_node])
                heappush(min_heap, (dist, next_node, current))

    return adj_list


# dfs_traversal function is used to perform Depth First Search (DFS) traversal on the MST
def dfs_traversal(adj_list: List[List[int]], start: int = 0) -> List[int]:
    visited = [False] * len(adj_list)
    route = []

    def dfs(node: int):
        visited[node] = True
        route.append(node)
        for neighbor in adj_list[node]:
            if not visited[neighbor]:
                dfs(neighbor)

    dfs(start)
    return route


# generate_route function is used to generate the route based on the DFS traversal
def generate_route(coordinates: List[Tuple[int, int]]) -> List[int]:
    mst = construct_mst(coordinates) 
    route = dfs_traversal(mst)       
    route.append(route[0])           
    return route


# calculate_total_distance function is used to calculate the total distance of the generated route
def calculate_total_distance(route: List[int], coordinates: List[Tuple[int, int]]) -> float:
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += euclidean_distance(coordinates[route[i]], coordinates[route[i + 1]])
    return total_distance

