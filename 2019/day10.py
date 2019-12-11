#!/usr/bin/env python

import argparse
import math
from collections import defaultdict


parser = argparse.ArgumentParser()
parser.add_argument('infile', type=str)


ASTEROID = 1
EMPTY = 0


def display(grid, in_sight, mapping=None):
    if mapping is None:
        mapping = {0: ' ', 1: '$'}
    max_x, max_y = max(grid, key=lambda k: k[0])[0], max(grid, key=lambda k: k[1])[1]
    min_x, min_y = min(grid, key=lambda k: k[0])[0], min(grid, key=lambda k: k[1])[1]
    lines = []
    for y in range(min_y, max_y + 1):
        line = ''
        for x in range(min_x, max_x + 1):
            if (x, y) in in_sight:
                line += str(len(in_sight[(x, y)]))
            else:
                line += mapping[grid[(x, y)]]
        lines.append(line)
    for line in lines:
        print(line)

    a = input("which one?")
    cx, cy = [int(x) for x in a.split(',')]
    while True:
        print()
        lines = []
        for y in range(min_y, max_y + 1):
            line = ''
            for x in range(min_x, max_x + 1):
                if (x, y) in in_sight[(cx, cy)]:
                    line += 'O'
                elif (x, y) == (cx, cy):
                    line += '$'
                else:
                    line += mapping[grid[(x, y)]]
            lines.append(line)
        for line in lines:
            print(line)
        a = input("which one?")
        cx, cy = [int(x) for x in a.split(',')]


def prep_data(blob):
    asteroid_map = {}
    for y, line in enumerate(blob.splitlines()):
        for x, value in enumerate(line.strip()):
            asteroid_map[(x, y)] = {
                '#': ASTEROID,
                '.': EMPTY
            }[value]
    return asteroid_map


def can_see(source, target, asteroid_map):
    """
    A can see B if there is nothing in increments of x_dist // gcd(x_distance, y_distance), y_dist // gcd(x_distance, y_distance)

    optimisations:
        if y_dist == 1: A and B can always see eachother
        if x_dist == 1: A and B can always see eachother
        if y_dist == x_dist, increments are (1, 1)
        if gcd == 1, A and B can see eachother?
    """
    x_dist, y_dist = abs(source[0] - target[0]), abs(source[1] - target[1])
    west, east = min(source, target), max(source, target)
    if x_dist == 1 or y_dist == 1:
        return True

    steps = math.gcd(x_dist, y_dist)
    if abs(x_dist - y_dist) == 1:
        return True
    else:
        x_steps, y_steps = x_dist // steps, y_dist // steps
        path = []
        y_steps *= (1 if west[1] <= east[1] else -1)  # go north if we're southwest
        x, y = west[0] + x_steps, west[1] + y_steps
        while (x, y) in asteroid_map and (x, y) != east:
            path.append(asteroid_map[(x, y)])
            x += x_steps
            y += y_steps

        return sum(path) == 0


def solve(asteroid_map):
    """
    if A can see B, B can see A
    """
    asteroids = set([k for k, v in asteroid_map.items() if v == ASTEROID])
    in_sight = defaultdict(set)  # (x, y) => set([(x, y)])
    for source in asteroids:
        for target in (asteroids - set([source]) - in_sight[source]):
            if can_see(source, target, asteroid_map):
                in_sight[source].add(target)
                in_sight[target].add(source)

    visible = max(in_sight.items(), key=lambda k: len(k[1]))[1]
    return len(visible)


if __name__ == '__main__':
    args = parser.parse_args()
    data = prep_data(open(args.infile).read())
    print("Part 1: {:d}".format(solve(data)))
