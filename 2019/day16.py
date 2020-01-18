#!/usr/bin/env python

import argparse
import numpy as np
from itertools import cycle


parser = argparse.ArgumentParser()
parser.add_argument('infile', type=str)
parser.add_argument('n_phases', type=int)
parser.add_argument('repetitions', type=int)


def prep_data(blob):
    return [int(x) for x in blob.strip()]


def get_transform(m):
    rep = [0, 1, 0, -1]
    transform = np.ndarray((m, m))
    for x in range(m):
        pattern = cycle(sum(zip(*[rep for j in range(x + 1)]), ()))
        next(pattern)

        for y in range(m):
            transform[y][x] = next(pattern)
    return transform


def solve(data, n_phases, repetitions):
    """
    1xm dot mxm -> 1xm
    """
    data *= repetitions
    m = len(data)
    result = np.ndarray((1, m))
    result[:] = data
    transform = get_transform(m)

    while n_phases:
        result = np.mod(abs(np.dot(result, transform)), 10)
        n_phases -= 1
        print(n_phases)

    result = result[0].tolist()
    return "".join([str(int(x)) for x in result[:8]])


if __name__ == '__main__':
    args = parser.parse_args()
    data = prep_data(open(args.infile).read())
    print("Part 1: {}".format(solve(data, args.n_phases, args.repetitions)))
