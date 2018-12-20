import json
import math
import sys
from collections import defaultdict, Counter

TREE = 0
LUMBERYARD = 1
OPEN = 2


class Acre(object):
    def __init__(self, grid, x, y):
        self.x = x
        self.y = y
        self.grid = grid

    @property
    def maxxy(self):
        return int(math.sqrt(len(self.grid)))

    def out_of_bounds(self, x, y):
        return x < 0 or x >= self.maxxy or y < 0 or y >= self.maxxy

    def neighbours(self):
        for x, y in [
            (-1, -1),
            (1, 1),
            (0, 1),
            (1, 0),
            (-1, 1),
            (1, -1),
            (-1, 0),
            (0, -1),
        ]:
            c = (self.x + x, self.y + y)
            if not self.out_of_bounds(*c):
                yield c

    def next_state(self):
        """
        Must return class of next state
        """
        raise NotImplementedError


class Tree(Acre):
    state = TREE

    def next_state(self):
        cnt = 0
        for n in self.neighbours():
            if self.grid[n].state == LUMBERYARD:
                cnt += 1
            if cnt >= 3:
                return LumberYard
        return Tree


class Open(Acre):
    state = OPEN

    def next_state(self):
        cnt = 0
        for n in self.neighbours():
            if self.grid[n].state == TREE:
                cnt += 1
            if cnt >= 3:
                return Tree
        return Open


class LumberYard(Acre):
    state = LUMBERYARD

    def next_state(self):
        tree_cnt = 0
        lumb_cnt = 0
        for n in self.neighbours():
            if self.grid[n].state == TREE:
                tree_cnt += 1
            elif self.grid[n].state == LUMBERYARD:
                lumb_cnt += 1
            if tree_cnt >= 1 and lumb_cnt >= 1:
                return LumberYard
        return Open


def get_resource_value(grid):
    return sum(
            [1 for x in grid.values() if x.state == TREE]
        ) * sum(
            [1 for x in grid.values() if x.state == LUMBERYARD]
        )


def compile_next_grid(grid):
    next_grid = {}
    for coordinate, acre in grid.items():
        # bind acre to grid and grid to acre
        next_grid[coordinate] = acre.next_state()(next_grid, *coordinate)
    return next_grid


char2class = {
    '#': LumberYard,
    '.': Open,
    '|': Tree
}


if __name__ == '__main__':
    data = open(sys.argv[1]).read().splitlines()
    grid = {}

    for y, line in enumerate(data):
        for x, char in enumerate(line.strip()):
            # bind acre to grid and grid to acre
            grid[(x, y)] = char2class[char](grid, x, y)

    for i in range(10):
        grid = compile_next_grid(grid)

    resource_value = get_resource_value(grid)
    print("Part 1: " + str(resource_value))

    # Assume the thing stabilizes at some point and if we see a recurring value
    # on a multiple of the target we can fast forward
    target_minutes = 1000000000 - 1
    i += 1
    values_seen_counts = Counter()
    while i < target_minutes:
        grid = compile_next_grid(grid)
        resource_value = get_resource_value(grid)
        values_seen_counts[resource_value] += 1
        if target_minutes % i == 0 and values_seen_counts[resource_value] > 5:
            break
        i += 1
    resource_value = get_resource_value(grid)
    print("Part 2: " + str(resource_value))
