#!/usr/bin/env python

import argparse


parser = argparse.ArgumentParser()
parser.add_argument('infile', type=str)


def prep_data(blob):
    paths = []
    for wire in blob.splitlines():
        if wire:
            x, y = 0, 0
            path = set()
            steps_taken = 1
            for definition in wire.split(','):
                direction, steps = definition[0], int(definition[1:])
                while steps:
                    # dont add 0, 0
                    x, y = {
                        'U': lambda _x, _y: (_x, _y - 1),
                        'D': lambda _x, _y: (_x, _y + 1),
                        'L': lambda _x, _y: (_x - 1, _y),
                        'R': lambda _x, _y: (_x + 1, _y),
                    }[direction](x, y)
                    path.add((x, y, steps_taken))
                    steps -= 1
                    steps_taken += 1
            paths.append(path)
    return paths


def manhattan_distance(p1, p2):
    return sum([
        abs(p1[0] * -1 + p2[0]),
        abs(p1[1] * -1 + p2[1]),
    ])


def solve(wires):
    w1, w2 = wires
    w1 = set([(x[0], x[1]) for x in w1])
    w2 = set([(x[0], x[1]) for x in w2])
    return min([manhattan_distance(x, (0, 0)) for x in w1 & w2])


def solve2(wires):
    w1, w2 = wires
    w1_dists, w2_dists = {}, {}
    intersections = set([(x[0], x[1]) for x in w1]) & set([(x[0], x[1]) for x in w2])
    for x, y, d in w1:
        if (x, y) in intersections:
            w1_dists[(x, y)] = min(w1_dists.get((x, y), 1 << 64), d)
    for x, y, d in w2:
        if (x, y) in intersections:
            w2_dists[(x, y)] = min(w2_dists.get((x, y), 1 << 64), d)
    return min([w1_dists[c] + w2_dists[c] for c in intersections])


if __name__ == '__main__':
    args = parser.parse_args()
    data = prep_data(open(args.infile).read())
    print("Part 1: {}".format(solve(data)))
    print("Part 2: {}".format(solve2(data)))
