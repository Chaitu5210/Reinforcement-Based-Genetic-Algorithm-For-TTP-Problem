import math
from typing import List, Tuple
from heapq import heappop, heappush

# Step 1: Compute Euclidean Distance
def euclidean_distance(coord1: Tuple[int, int], coord2: Tuple[int, int]) -> float:
    return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)

# Step 2: Construct MST using Prim's Algorithm
def construct_mst(coordinates: List[Tuple[int, int]]) -> List[List[int]]:
    n = len(coordinates)
    adj_list = [[] for _ in range(n)]
    visited = [False] * n
    min_heap = [(0, 0, -1)]  # (weight, current_node, parent_node)

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

# Step 3: Perform DFS to Derive the Route
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

# Main Function to Generate the Route
def generate_route(coordinates: List[Tuple[int, int]]) -> List[int]:
    mst = construct_mst(coordinates)  # Build MST
    route = dfs_traversal(mst)        # Perform DFS to get the route
    route.append(route[0])            # Return to the starting point
    return route

# Calculate Total Distance of the Route
def calculate_total_distance(route: List[int], coordinates: List[Tuple[int, int]]) -> float:
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += euclidean_distance(coordinates[route[i]], coordinates[route[i + 1]])
    return total_distance

