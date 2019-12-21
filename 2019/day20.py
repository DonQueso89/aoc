#!/usr/bin/env python

import argparse
import heapq
import string
from collections import defaultdict


parser = argparse.ArgumentParser()
parser.add_argument('infile', type=str)


OPEN = 0
WALL = 1
NOTHING = 2
WARP = 3


def prep_data(blob):
    warps = defaultdict(list)
    maze = {}
    blob = blob.splitlines()
    start = (0, 0)
    for y, line in enumerate(blob):
        for x, c in enumerate(line):
            if c == '#':
                maze[(x, y)] = WALL
            elif c == '.':
                maze[(x, y)] = OPEN

                for nx, ny, nxx, nyy, order in [
                    (x - 1, y, x - 2, y, 1),
                    (x + 1, y, x + 2, y, 0),
                    (x, y + 1, x, y + 2, 0),
                    (x, y - 1, x, y - 2, 1),
                ]:
                    if blob[ny][nx] == 'A' and blob[nyy][nxx] == 'A':
                        start = (x, y)
                        maze[(nx, ny)] = NOTHING
                    elif blob[ny][nx] == 'Z' and blob[nyy][nxx] == 'Z':
                        target = (x, y)
                        maze[(nx, ny)] = NOTHING
                    elif blob[ny][nx] in string.ascii_uppercase:
                        if order == 0:
                            warps[(blob[ny][nx], blob[nyy][nxx])].append((x, y))
                        if order == 1:
                            warps[(blob[nyy][nxx], blob[ny][nx])].append((x, y))
                        maze[(nx, ny)] = WARP
            else:
                maze[(x, y)] = NOTHING
    _warps = {}
    for _from, to in warps.values():
        _warps[_from] = to
        _warps[to] = _from
    return start, target, _warps, maze


def solve(start, target, warps, maze):
    queue = [start + (0, )]
    pop = heapq.heappop
    push = heapq.heappush
    visited = set()
    while True:
        new_queue = []

        while queue:
            x, y, d = pop(queue)

            if (x, y) == target:
                return d

            if (x, y) in warps and warps[(x, y)] not in visited:
                push(new_queue, warps[(x, y)] + (d + 1, ))

            for nx, ny in [
                (x - 1, y),
                (x + 1, y),
                (x, y + 1),
                (x, y - 1),
            ]:
                area = maze[(nx, ny)]

                if area == OPEN and (nx, ny) not in visited:
                    push(new_queue, (nx, ny, d + 1))
            visited.add((x, y))
        queue = new_queue


def solve2(start, target, warps, maze):
    start += (0, )  # extra dimension: level
    target += (0, )
    max_x = max(maze)[0]
    max_y = max(maze)[1]

    inner_warps = {k: v for k, v in warps.items() if 5 < k[0] < max_x - 5 and 5 < k[1] < max_y - 5}
    outer_warps = {k: v for k, v in warps.items() if k not in inner_warps}

    inner_maze = {k: v for k, v in maze.items()}
    inner_maze[start] = WALL
    inner_maze[target] = WALL
    outer_maze = maze

    for x, y in outer_warps:
        outer_maze[(x, y)] = WALL

    queue = [start + (0, )]
    pop = heapq.heappop
    push = heapq.heappush
    visited = set()

    while True:
        new_queue = []

        while queue:
            x, y, l, d = pop(queue)

            if (x, y, l) == target:
                return d

            if (x, y) in inner_warps and inner_warps[(x, y)] + (l + 1, ) not in visited:
                push(new_queue, warps[(x, y)] + (l + 1, d + 1, ))
            if (x, y) in outer_warps and outer_warps[(x, y)] + (l - 1, ) not in visited:
                push(new_queue, warps[(x, y)] + (l - 1, d + 1, ))

            if l == 0:
                maze = outer_maze
            else:
                maze = inner_maze

            for nx, ny in [
                (x - 1, y),
                (x + 1, y),
                (x, y + 1),
                (x, y - 1),
            ]:
                area = maze[(nx, ny)]

                if area == OPEN and (nx, ny, l) not in visited:
                    push(new_queue, (nx, ny, l, d + 1))
            visited.add((x, y, l))

        queue = new_queue


if __name__ == '__main__':
    args = parser.parse_args()
    data = prep_data(open(args.infile).read())
    print("Part 1: {:d}".format(solve(*data)))
    print("Part 2: {:d}".format(solve2(*data)))
