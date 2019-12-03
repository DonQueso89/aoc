import time
import argparse
import heapq
from collections import defaultdict
from functools import partial

parser = argparse.ArgumentParser(description='Solve day 22')
parser.add_argument('depth', type=int, help='depth of cave')
parser.add_argument('targetX', type=int, help='target x coordinate')
parser.add_argument('targetY', type=int, help='target y coordinate')


'''
start with the torch equipped at (0, 0)
In rocky regions, you can use the climbing gear or the torch. You cannot use neither (you'll likely slip and fall).
In wet regions, you can use the climbing gear or neither tool. You cannot use the torch (if it gets wet, you won't have a light source).
In narrow regions, you can use the torch or neither tool. You cannot use the climbing gear (it's too bulky to fit).
At the end, you need the torch
'''


ROCK = 0
WET = 1
NARROW = 2

NEITHER = 0
TORCH = 1
CLIMBING_GEAR = 2

valid_for_rock = set([CLIMBING_GEAR, TORCH])
valid_for_wet = set([CLIMBING_GEAR, NEITHER])
valid_for_narrow = set([TORCH, NEITHER])

tools_for = {
    ROCK: valid_for_rock,
    WET: valid_for_wet,
    NARROW: valid_for_narrow
}

dm = {
    ROCK: '.',
    WET: '~',
    NARROW: '|'
}

tm = {
    NEITHER: 'N',
    TORCH: 'F',
    CLIMBING_GEAR: 'C',
}


def neighbours(cave_map, x, y, current_tool):
    """ 
    Treat each possible (x, y, tool) combo as a separate vertex
    """
    candidates = set([])
    for offsetX, offsetY in [
        (0, 1),
        (1, 0),
        (-1, 0),
        (0, -1)
    ]:
        sx, sy = x + offsetX, y + offsetY
        if (sx, sy) not in cave_map:
            continue
        if current_tool in tools_for[cave_map[(sx, sy)]]:
            candidates.add((sx, sy, current_tool))
    for tool in tools_for[cave_map[(x, y)]] - set([current_tool]):
        candidates.add((x, y, tool))

    for c in candidates:
        yield c


def _get_erosion_level(erosion_levels, depth, x, y):
    if y == 0:
        return (x * 16807 + depth) % 20183
    if x == 0:
        return (y * 48271 + depth) % 20183
    return (erosion_levels[(x - 1, y)] * erosion_levels[(x, y - 1)] + depth) % 20183


def display(cave_map, tx, ty, cx, cy, tool):
    result = ""
    for y in range(0, max(cave_map.keys(), key=lambda k: k[1])[1] + 1):
        result += '\n'
        for x in range(0, max(cave_map.keys(), key=lambda k: k[0])[0] + 1):
            if (cx, cy) == (x, y):
                result += " " + str(tm[tool])
            elif (tx, ty) == (x, y):
                result += " T"
            else:
                result += (" " + str(dm[cave_map[(x, y)]]))


def display_queue(pq, cave_map, tx, ty, tt, sx, sy, st, visited):
    max_x = max(pq, key=lambda k: k[0])[0]
    max_y = max(pq, key=lambda k: k[1])[1]
    for y in range(max_y + 1):
        line = ""
        for x in range(max_x + 1):
            for tool in tools_for[cave_map[(x, y)]]:
                if (x, y, tool) == (tx, ty, tt):
                    line += ("||%04d||" % pq.get((x, y, tool), (0, 0))[0])
                elif (x, y, tool) == (sx, sy, st):
                    line += ("->%04d<-" % pq.get((x, y, tool), (0, 0))[0])
                elif (x, y, tool) in visited:
                    line += (" <%04d> " % pq.get((x, y, tool), (0, 0))[0])
                else:
                    line += ("  %04d  " % pq.get((x, y, tool), (0, 0))[0])
            print(line)


def generate_cave_map(depth, tx, ty):
    erosion_levels = defaultdict(int)
    erosion_levels[(0, 0)] = 0 + depth

    get_erosion_level = partial(_get_erosion_level, erosion_levels, depth)

    # Calculate west and north borders first to avoid the overhead of checking
    # whether the coordinate is the cavemouth on every iteration
    # North border
    for y in range(0, 1):
        for x in range(1, tx + 1):
            erosion_levels[(x, y)] = get_erosion_level(x, y)

    # West border
    for y in range(1, ty + 1):
        for x in range(0, 1):
            erosion_levels[(x, y)] = get_erosion_level(x, y)

    for y in range(1, ty + 1):
        for x in range(1, tx + 1):
            erosion_levels[(x, y)] = get_erosion_level(x, y)

    erosion_levels[(tx, ty)] = 0 + depth
    cave_map = {coordinate: el % 3 for coordinate, el in erosion_levels.items()}
    return cave_map


def solve(depth, tx, ty):
    return sum(list(generate_cave_map(depth, tx, ty).values()))


def _distance(c1, c2):
    distance = 0
    x1, y1, t1 = c1
    x2, y2, t2 = c2
    if (x1, y1) != (x2, y2):
        distance += 1
    if t1 != t2:
        distance += 7
    return distance


def dijkstra(start, target, cave_map):
    """
    Init priority queue with start node at 0 and all others at Infinity
    PQ keeps track of where we've been by storing the previous node and the shortest distance
    1) For each neighbour of node with closest distance
    2) If distance to next node is smaller than current distance in PQ, replace
        with distance and this node as previous node
    Every time all neighbours for the node under consideration have been checked,
    remove the node from the PQ

    """
    large_int = 1 << 64
    pq = []  # {node: (distance_from_source, previous_node)}
    push = heapq.heappush
    pop = heapq.heappop
    push(pq, (0, start))
    shortest_paths = {}  # keep track of final shortest paths
    _neighbours = partial(neighbours, cave_map)
    while pq:
        distance, candidate = pop(pq)
        if candidate in shortest_paths:
            continue
        shortest_paths[candidate] = distance
        if candidate == target:
            return shortest_paths[target]

        for neighbour in list(_neighbours(*candidate)):
            distance += _distance(neighbour, candidate)
            if distance < shortest_paths.get(neighbour, large_int):
                shortest_paths[neighbour] = distance


def solve2(depth, tx, ty):
    cave_map = generate_cave_map(depth, depth // 20, depth // 20)
    return dijkstra((0, 0, TORCH), (tx, ty, TORCH), cave_map)


if __name__ == '__main__':
    args = parser.parse_args()
    depth, tx, ty = args.depth, args.targetX, args.targetY
    print("Part 1: " + str(solve(depth, tx, ty)))
    print("Part 2: " + str(solve2(depth, tx, ty)))
