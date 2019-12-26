#!/usr/bin/env python

import argparse


parser = argparse.ArgumentParser()
parser.add_argument('infile', type=str)


EMPTY = 0
BUG = 1
INNER_STACK = 2
OUTER_STACK = 3


def prep_data(blob):
    grid = {}
    for y, line in enumerate(blob.splitlines()):
        for x, c in enumerate(line):
            grid[(x, y)] = EMPTY if c == '.' else BUG
    return grid


def solve(grid):
    prev = set([])
    bio_rating = ''.join([str(x[1]) for x in sorted(grid.items(), key=lambda k: (k[0][1], k[0][0]))][::-1])
    prev.add(int(bio_rating, 2))

    while True:
        new = {}
        for x, y in grid:
            state = grid[(x, y)]
            nbugs = sum([
                grid.get((nx, ny)) == BUG for nx, ny in [
                    (x - 1, y),
                    (x + 1, y),
                    (x, y + 1),
                    (x, y - 1),
                ]
            ])

            if state == BUG and nbugs != 1:
                state = EMPTY
            elif state == EMPTY and nbugs in (1, 2):
                state = BUG

            new[(x, y)] = state

        grid = new
        bio_rating = int(''.join([str(x[1]) for x in sorted(grid.items(), key=lambda k: (k[0][1], k[0][0]))][::-1]), 2)
        if bio_rating in prev:
            break
        prev.add(bio_rating)

    return bio_rating


def solve2(grid):
    grid[(2, 2)] = INNER_STACK
    for x, y in grid:
        grid[(x, y)] += (0, )

    """
    Inner: also check all outer of level + 1
    Outer: check inner of level - 1
    """

    while True:
        new = {}
        for x, y, level in grid:
            state = grid[(x, y)]
            nbugs = sum([
                grid.get((nx, ny, level)) == BUG for nx, ny in [
                    (x - 1, y),
                    (x + 1, y),
                    (x, y + 1),
                    (x, y - 1),
                ]
            ])

            if state == BUG and nbugs != 1:
                state = EMPTY
            elif state == EMPTY and nbugs in (1, 2):
                state = BUG

            new[(x, y)] = state

        grid = new

    return sum(grid.values())


if __name__ == '__main__':
    args = parser.parse_args()
    data = prep_data(open(args.infile).read())
    print("Part 1: {:d}".format(solve(data)))
    print("Part 2: {:d}".format(solve2(data)))
