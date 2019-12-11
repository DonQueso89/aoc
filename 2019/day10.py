#!/usr/bin/env python

import argparse
from math import gcd


parser = argparse.ArgumentParser()
parser.add_argument('infile', type=str)


def prep_data(blob):
    asteroid_map = {}
    for y, line in enumerate(blob.splitlines()):
        for x, value in enumerate(line):
            asteroid_map[(x, y)] = {
                '#': 1,
                '.': 0
            }[value]
    return asteroid_map


def solve(asteroids):
    """
    A can see B if there is nothing in increments of x_dist // gcd(x_distance, y_distance), y_dist // gcd(x_distance, y_distance)

    optimisations:
        if y_dist == 1: A and B can always see eachother
        if x_dist == 1: A and B can always see eachother
        if y_dist == x_dist, increments are (1, 1)
        if gcd == 1, A and B can see eachother?

    if A can see B, B can see A
    """
    connected = {}






if __name__ == '__main__':
    args = parser.parse_args()
    data = prep_data(open(args.infile).read())
    print("Part 1: {:d}".format(solve(data)))
