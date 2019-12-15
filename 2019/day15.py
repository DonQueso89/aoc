#!/usr/bin/env python

import argparse
import heapq
import random
from day5 import prep_data, intcode_runtime
from collections import defaultdict


parser = argparse.ArgumentParser()
parser.add_argument('infile', type=str)


NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4


DIRS = [NORTH, SOUTH, WEST, EAST]


BLOCKED = 0
EMPTY = 1
JACKPOT = 2
UNKNOWN = 3
OXYGEN = 4


def display(grid, mapping=None):
    if mapping is None:
        mapping = {0: ' ', 1: '$'}
    max_x, max_y = max(grid, key=lambda k: k[0])[0], max(grid, key=lambda k: k[1])[1]
    min_x, min_y = min(grid, key=lambda k: k[0])[0], min(grid, key=lambda k: k[1])[1]
    print("$" * (max_x - min_x))
    lines = []
    for y in range(min_y, max_y + 1):
        line = ''
        for x in range(min_x, max_x + 1):
            line += mapping[grid.get((x, y), UNKNOWN)]
        lines.append(line)
    for line in reversed(lines):
        print(line)
    print("$" * (max_x - min_x))


class Droid:
    def __init__(self, program, x=0, y=0, pointer=None, relative_base=None):
        self.pointer = pointer
        self.relative_base = relative_base
        self.program = {k: v for k, v in program.items()}
        self.x = x
        self.y = y

    def intcode_input(self, _input):
        return {
            'data': self.program,
            '_inputs': [_input],
            'pointer': self.pointer,
            'relative_base': self.relative_base,
            'feedback_mode': True
        }

    def copy(self):
        return Droid(
            self.program,
            self.x,
            self.y,
            self.pointer,
            self.relative_base
        )

    def go(self, _dir):
        self.x, self.y = {
            NORTH: (self.x, self.y - 1),
            SOUTH: (self.x, self.y + 1),
            WEST: (self.x - 1, self.y),
            EAST: (self.x + 1, self.y),
        }[_dir]
        status, self.pointer, self.program, self.relative_base = intcode_runtime(**self.intcode_input(_dir))
        return self, status


def droid_fill(program):
    """
    Flood fill  with droids, keeping program state for each scout
    """
    grid = {(0, 0): EMPTY}
    distances = defaultdict(int, {(0, 0): 0})  # (x, y) => d
    droids = {(0, 0): Droid(program)}
    queue = [(0, 0)]
    pop = heapq.heappop
    push = heapq.heappush
    oxygen_system = None

    while queue:
        x, y = pop(queue)
        distance = distances[(x, y)]
        droid = droids.pop((x, y))  # program state for stuff in the queue
        nav = {
            NORTH: (x, y - 1),
            SOUTH: (x, y + 1),
            WEST: (x - 1, y),
            EAST: (x + 1, y),
        }

        for direction in DIRS:
            nx, ny = nav[direction]
            if (nx, ny) in distances:
                continue

            scout, status = droid.copy().go(direction)
            if status == JACKPOT:
                oxygen_system = (nx, ny)
                grid[(nx, ny)] = status
                distances[(nx, ny)] = distance + 1
            elif status == BLOCKED:
                grid[(nx, ny)] = status
                distances[(nx, ny)] = None
            elif status == EMPTY:
                grid[(nx, ny)] = status
                distances[(nx, ny)] = distance + 1
                droids[(nx, ny)] = scout
                push(queue, (nx, ny))
            else:
                raise Exception('Unknown output')

    #display(grid, mapping={BLOCKED: '#', EMPTY: '.', UNKNOWN: '?', JACKPOT: 'X'})
    return oxygen_system, distances[oxygen_system], grid


def oxygen_fill(program):
    """
    Regular flood fill
    """
    oxygen_system, p1, grid = droid_fill(program)
    queue = [oxygen_system]
    visited = set([oxygen_system])
    ticks = 0

    while queue:
        new_queue = []
        while queue:
            x, y = queue.pop()
            nav = {
                NORTH: (x, y - 1),
                SOUTH: (x, y + 1),
                WEST: (x - 1, y),
                EAST: (x + 1, y),
            }

            for _dir in DIRS:
                nx, ny = nav[_dir]
                if (nx, ny) in visited:
                    continue
                if grid[(nx, ny)] == BLOCKED:
                    continue

                visited.add((nx, ny))
                area = grid[(nx, ny)]
                if area == EMPTY:
                    new_queue.append((nx, ny))
        queue = new_queue
        if queue:
            ticks += 1

    return p1, ticks


def solve(program):
    return oxygen_fill(program)


if __name__ == '__main__':
    args = parser.parse_args()
    data = prep_data(open(args.infile).read())
    print("Part 1: {:d}\nPart 2: {:d}".format(*solve(data)))
