import time
import argparse
import heapq
import networkx 
from collections import defaultdict
from functools import partial

parser = argparse.ArgumentParser(description='Solve day 22')
parser.add_argument('depth', type=int, help='depth of cave')
parser.add_argument('targetX', type=int, help='target x coordinate')
parser.add_argument('targetY', type=int, help='target y coordinate')


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
    print(result)


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


def generate_cave_map(depth, tx, ty, max_x, max_y):
    erosion_levels = defaultdict(int)
    erosion_levels[(0, 0)] = depth % 20183

    get_erosion_level = partial(_get_erosion_level, erosion_levels, depth)

    # North border
    for x in range(1, max_x):
        erosion_levels[(x, 0)] = get_erosion_level(x, 0)

    # West border
    for y in range(1, max_y):
        erosion_levels[(0, y)] = get_erosion_level(0, y)

    for y in range(1, max_y):
        for x in range(1, max_x):
            erosion_levels[(x, y)] = get_erosion_level(x, y)

    erosion_levels[(tx, ty)] = depth % 20183
    cave_map = {coordinate: el % 3 for coordinate, el in erosion_levels.items()}
    return cave_map


def get_graph(grid):
    G = networkx.Graph()
    for (x, y), _type in grid.items():
        for tool in tools_for[_type]:
            G.add_node((x, y, tool))

            for nx, ny in [
                (x - 1, y),
                (x + 1, y),
                (x, y - 1),
                (x, y + 1),
            ]:
                if (nx, ny) in grid:
                    for ntool in tools_for[grid[(nx, ny)]]:
                        if ntool == tool:
                            G.add_edge(
                                (x, y, tool),
                                (nx, ny, ntool),
                                weight=1
                            )

            for ntool in tools_for[_type]:
                if ntool != tool:
                    G.add_edge((x, y, tool), (x, y, ntool), weight=7)
    return G




def solve(depth, tx, ty):
    grid = generate_cave_map(depth, tx, ty, depth, depth)
    #display(grid, tx, ty, 0, 0, 1)

    G = get_graph(grid)
    print("NetworkX says: ",
            networkx.shortest_path_length(G, (0, 0, TORCH), (tx, ty, TORCH), weight='weight'))

    pq = [(0, 0, 0, TORCH)]  # distance, x, y, tool
    push = heapq.heappush
    pop = heapq.heappop
    visited = set()
    target = (tx, ty, TORCH)
    p1 = sum([v for k, v in grid.items() if k[0] <= tx and k[1] <= ty])
    shortest = {}
    large_int = 1 << 64

    while True:
        d, x, y, tool = pop(pq)
        if (x, y, tool) in visited:
            continue

        if (x, y, tool) == target:
            return p1, d

        visited.add((x, y, tool))
        shortest[(x, y, tool)] = d
        neighbours = set([])
        for nx, ny in [
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1),
        ]:
            if (nx, ny) not in grid:
                continue

            if tool in tools_for[grid[(nx, ny)]] and (nx, ny, tool) not in visited:
                neighbours.add((d + 1, nx, ny, tool))

        for t in (tools_for[grid[(x, y)]] - set([tool])):
            if (x, y, t) not in visited:
                neighbours.add((d + 7, x, y, t))

        for d, nx, ny, tool in neighbours:
            if d < shortest.get((nx, ny, tool), large_int):
                shortest[(nx, ny, tool)] = d
            push(pq, (d, nx, ny, tool))

    raise Exception("never hit target")


if __name__ == '__main__':
    args = parser.parse_args()
    depth, tx, ty = args.depth, args.targetX, args.targetY
    print("Part 1: {:d}\nPart 2: {:d}".format(*solve(depth, tx, ty)))
