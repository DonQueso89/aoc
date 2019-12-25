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


if __name__ == '__main__':
    args = parser.parse_args()
    data = open(args.infile).read()
    print("Part 1: {:d}".format(solve(data)))
