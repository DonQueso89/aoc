#!/usr/bin/env python

import argparse
import numpy as np
from day5 import prep_data, intcode_runtime
from collections import defaultdict


parser = argparse.ArgumentParser()
parser.add_argument('infile', type=str)
parser.add_argument('input', type=int)


dirs = 'SWNE'


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
            line += mapping[grid[(x, y)]]
        lines.append(line)
    for line in reversed(lines):
        print(line)
    print("$" * (max_x - min_x))


def solve(program, _input):
    visited = set()
    grid = defaultdict(int)
    pointer, relative_base = 0, 0
    x, y = 0, 0
    direction = 2
    grid[(0, 0)] = _input
    while pointer is not None:
        visited.add((x, y))
        color, pointer, program, relative_base = intcode_runtime(
            program,
            [grid[(x, y)]],
            pointer=pointer,
            feedback_mode=True,
            relative_base=relative_base
        )

        if pointer is None:
            print('Part 2:')
            display(grid)
            return len(visited)

        go_right, pointer, program, relative_base = intcode_runtime(
            program,
            [],
            pointer=pointer,
            feedback_mode=True,
            relative_base=relative_base
        )
        grid[(x, y)] = color
        direction = (direction + (1 if go_right else -1)) % 4

        x, y = {
            'S': (x, y-1),
            'N': (x, y+1),
            'E': (x+1, y),
            'W': (x-1, y),
        }[dirs[direction]]

    print('Part 2:')
    display(grid)
    return len(visited)


if __name__ == '__main__':
    args = parser.parse_args()
    data = prep_data(open(args.infile).read())
    print("Part 1: {:d}".format(solve(data, args.input)))
