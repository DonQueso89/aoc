#!/usr/bin/env python

import argparse


parser = argparse.ArgumentParser()
parser.add_argument('infile', type=str)


def prep_data(blob):
    for g in blob.splitlines():
        if g:
            yield(int(g))


def solve(data):
    return sum([x//3-2 for x in data])


def solve2(data):
    if sum(data) == 0:
        return 0
    metafuel = [max(x//3-2, 0) for x in data]
    return sum(metafuel) + solve2(metafuel)


if __name__ == '__main__':
    args = parser.parse_args()
    data = list(prep_data(open(args.infile).read()))
    print("Part 1: {:d}".format(solve(data)))
    print("Part 2: {:d}".format(solve2(data)))
