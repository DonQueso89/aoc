#!/usr/bin/env python

import argparse
import re


parser = argparse.ArgumentParser()
parser.add_argument('infile', type=str)
parser.add_argument('ticks', type=int)


def prep_data(blob):
    # {(x, y, z, xv, yv, zv), ...}
    return set(tuple(map(int, re.findall("[-]*\d+", line) + [0, 0, 0])) for line in blob.splitlines())


def solve(moons, ticks):
    while ticks:
        new_moons = set()
        for tx, ty, tz, txv, tyv, tzv in moons:
            for sx, sy, sz, _, _, _ in moons - set([(tx, ty, tz, txv, tyv, tzv)]):
                dx = 1 if sx > tx else -1 if sx < tx else 0
                dy = 1 if sy > ty else -1 if sy < ty else 0
                dz = 1 if sz > tz else -1 if sz < tz else 0
                txv += dx
                tyv += dy
                tzv += dz

            new_moons.add((tx + txv, ty + tyv, tz + tzv, txv, tyv, tzv))
        moons = new_moons
        ticks -= 1
    return sum([sum(map(abs, m[:3])) * sum(map(abs, m[3:])) for m in moons])


if __name__ == '__main__':
    args = parser.parse_args()
    data = prep_data(open(args.infile).read())
    print(data)
    print("Part 1: {:d}".format(solve(data, args.ticks)))
