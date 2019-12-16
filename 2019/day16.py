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


def solve(data, n_phases, repetitions):
    """
    1xm dot mxm -> 1xm
    """
    rep = [0, 1, 0, -1]
    offset = int("".join(map(str, data[:7]))) + 1
    data *= repetitions
    m = len(data)

    result = np.ndarray((1, m))
    result[:] = data
    transform = np.ndarray((m, m))
    print(m)

    for x in range(m):
        pattern = cycle(sum(zip(*[rep for j in range(x + 1)]), ()))
        next(pattern)

        for y in range(m):
            transform[y][x] = next(pattern)
    print("done compiling")

    while n_phases:
        result = np.mod(abs(np.dot(result, transform)), 10)
        n_phases -= 1
        print(n_phases)

    result = result[0].tolist()
    return "".join(map(lambda x: str(int(x)), result[:8])), "".join(map(lambda x: str(int(x)), result[offset:offset+8]))


if __name__ == '__main__':
    args = parser.parse_args()
    data = prep_data(open(args.infile).read())
    print("Part 1: {}".format(solve(data, args.n_phases, args.repetitions)))
