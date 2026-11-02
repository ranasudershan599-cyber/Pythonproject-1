"""Graph algorithms for the Flight Route Planner."""
from collections import deque
import heapq


def build_graph(routes, weight="distance_km", directed=False):
    """Build an adjacency list from list of route dicts."""
    graph = {}
    for row in routes:
        source, target = row["source"], row["destination"]
        edge = {"weight": float(row[weight]), "route": row}
        graph.setdefault(source, []).append((target, edge))
        graph.setdefault(target, [])
        if not directed:
            graph[target].append((source, {"weight": edge["weight"], "route": row}))
    return graph


def dijkstra(graph, start, goal):
    """Return (node path, total weight); O((V+E) log V) with a binary heap."""
    if start not in graph or goal not in graph:
        return None, float("inf")
    distances, previous = {start: 0.0}, {}
    queue = [(0.0, start)]
    while queue:
        distance, node = heapq.heappop(queue)
        if distance != distances.get(node):
            continue
        if node == goal:
            break
        for neighbor, edge in graph[node]:
            candidate = distance + edge["weight"]
            if candidate < distances.get(neighbor, float("inf")):
                distances[neighbor], previous[neighbor] = candidate, node
                heapq.heappush(queue, (candidate, neighbor))
    if goal not in distances:
        return None, float("inf")
    path, node = [], goal
    while node != start:
        path.append(node)
        node = previous[node]
    path.append(start)
    return path[::-1], distances[goal]


def bfs_fewest_legs(graph, start, goal):
    """Return a path with the fewest edges; O(V+E)."""
    if start not in graph or goal not in graph:
        return None
    queue, previous = deque([start]), {start: None}
    while queue:
        node = queue.popleft()
        if node == goal:
            path = []
            while node is not None:
                path.append(node)
                node = previous[node]
            return path[::-1]
        for neighbor, _ in graph[node]:
            if neighbor not in previous:
                previous[neighbor] = node
                queue.append(neighbor)
    return None


def dfs_path(graph, start, goal):
    """Return one available path using depth-first search; O(V+E)."""
    if start not in graph or goal not in graph:
        return None
    stack, previous = [start], {start: None}
    while stack:
        node = stack.pop()
        if node == goal:
            path = []
            while node is not None:
                path.append(node)
                node = previous[node]
            return path[::-1]
        for neighbor, _ in graph[node]:
            if neighbor not in previous:
                previous[neighbor] = node
                stack.append(neighbor)
    return None