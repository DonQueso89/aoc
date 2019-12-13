#!/usr/bin/env python

import argparse
import random
import time
from day5 import prep_data, intcode_runtime


parser = argparse.ArgumentParser()
parser.add_argument('infile', type=str)


BALL = 4
PADDLE = 3


def solve(program):
    pointer = 0
    relative_base = 0
    outputs = []
    while pointer is not None:
        output, pointer, program, relative_base = intcode_runtime(
            program,
            [],
            pointer=pointer,
            feedback_mode=True,
            relative_base=relative_base
        )
        outputs.append(output)
    return sum([x==2 for i, x in enumerate(outputs) if (i + 1) % 3 == 0])


def solve2(program):
    pointer = 0
    relative_base = 0
    outputs = []
    program[0] = 2
    grid = {}
    ball = (0, 0)
    paddle = (0, 0)
    inp = 0
    while pointer is not None:
        output, pointer, program, relative_base = intcode_runtime(
            program,
            [inp],
            pointer=pointer,
            feedback_mode=True,
            relative_base=relative_base
        )
        outputs.append(output)
        if len(outputs) == 3:
            tile_id, y, x = outputs.pop(), outputs.pop(), outputs.pop()
            grid[(x, y)] = tile_id
            if tile_id == BALL:
                ball = (x, y)
            if tile_id == PADDLE:
                paddle = (x, y)
            if ball[0] == paddle[0]:
                inp = 0
            elif ball[0] > paddle[0]:
                inp = 1
            else:
                inp = -1

    return grid[(-1, 0)]


if __name__ == '__main__':
    args = parser.parse_args()
    data = prep_data(open(args.infile).read())
    print("Part 1: {:d}".format(solve(data)))
    print("Part 2: {:d}".format(solve2(data)))
