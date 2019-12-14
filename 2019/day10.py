#!/usr/bin/env python

import argparse
import math
from collections import defaultdict


parser = argparse.ArgumentParser()
parser.add_argument('infile', type=str)


ASTEROID = 1
EMPTY = 0


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
    asteroids = set([k for k, v in asteroid_map.items() if v == ASTEROID])
    in_sight = defaultdict(set)  # (x, y) => set([(x, y)])
    for source in asteroids:
        for target in (asteroids - set([source]) - in_sight[source]):
            if can_see(source, target, asteroid_map):
                in_sight[source].add(target)
                in_sight[target].add(source)

    laser_base, visible = max(in_sight.items(), key=lambda k: len(k[1]))

    def sort_by_angle(k):
        k = math.atan2(laser_base[1] - k[1], laser_base[0] - k[0])
        if -math.pi <= k < math.pi / 2:
            return k + math.pi * 2.01
        return k - math.pi / 2

    visible = sorted(visible, key=sort_by_angle)
    return len(visible), visible[199][0] * 100 + visible[199][1]


if __name__ == '__main__':
    args = parser.parse_args()
    data = prep_data(open(args.infile).read())
    print("Part 1: {:d}\nPart 2: {:d}".format(*solve(data)))
