#!/usr/bin/env python

import argparse
from io import TextIOWrapper
from pathlib import Path

parser = argparse.ArgumentParser(description="day X")

parser.add_argument("input", type=str, help="input file")

dir_ = Path(__file__).parent


def neighbours(x, y):
    for c, d in [
        ((x + 1, y), "E"),
        ((x - 1, y), "W"),
        ((x, y + 1), "S"),
        ((x, y - 1), "N"),
    ]:
        yield c, d

def contiguous_groups(coords, level_dim, contiguous_dim):
    coords = sorted(coords, key=lambda x: (x[level_dim], x[contiguous_dim]))
    n = 0
    prev = None
    for c in coords:
        if prev is None or c[contiguous_dim] - prev[contiguous_dim] > 1 or c[level_dim] != prev[level_dim]:
            n += 1
        prev = c
    return n

def main(infp: TextIOWrapper, args: argparse.Namespace):
    inp = infp.read()

    grid = {}
    for y, line in enumerate(inp.splitlines()):
        for x, c in enumerate(line):
            grid[(x, y)] = c

    regions = []
    candidates = set(grid.keys())
    cur = None
    perimeters = []
    sides = []

    while candidates:
        if cur is None:
            cur = candidates.pop()
            regions.append(set([cur]))
            perimeters.append(0)
            sides.append({})

        e = grid[cur]
        for n, d in neighbours(*cur):
            if grid.get(n) == e:
                regions[-1].add(n)
            else:
                sides[-1].setdefault(d, set()).add(n)
                perimeters[-1] += 1


        candidates.discard(cur)
        _region_candidates = regions[-1] & candidates
        cur = _region_candidates.pop() if _region_candidates else None

    s = sum([len(r) * p for r, p in zip(regions, perimeters)])
    print(s)
    s = 0
    for r, side in zip(regions, sides):
        for d, coords in side.items():
            contiguous_dim = 0 if d in 'NS' else 1
            level_dim = int(not contiguous_dim)
            s += len(r) * contiguous_groups(coords, level_dim, contiguous_dim)
    
    print(s)

if __name__ == "__main__":
    args = parser.parse_args()
    infp = open(dir_ / args.input.split("/")[-1], "r")
    main(infp, args)
