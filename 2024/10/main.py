#!/usr/bin/env python

import argparse
from io import TextIOWrapper
from pathlib import Path

parser = argparse.ArgumentParser(description='day X')

parser.add_argument('input', type=str, help='input file')

dir_ = Path(__file__).parent

def num_hikes(grid, trailhead, unique=True):
    paths = [[trailhead]]
    completed = []
    while paths:
        visited = paths.pop()
        x, y = visited[-1]
        t = grid[(x, y)]
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            n = grid.get((nx, ny))
            if n == (t + 1) == 9:
                completed.append(visited + [(nx, ny)])
            elif n == (t + 1) and (nx, ny) not in visited:
                paths.append([*visited, (nx, ny)])
    
    if unique:
        return len(set([x[-1] for x in completed]))
    return len(completed)

def main(infp: TextIOWrapper, args: argparse.Namespace):
    inp = infp.read()

    grid = {}
    trailheads  = set()
    for y, line in enumerate(inp.splitlines()):
        for x, c in enumerate(line):
            c = int(c)
            grid[(x, y)] = c
            if c == 0:
                trailheads.add((x, y))

    print(sum(num_hikes(grid, th) for th in trailheads))
    print(sum(num_hikes(grid, th, unique=False) for th in trailheads))
    


if __name__ == '__main__':
    args = parser.parse_args()
    infp = open(dir_ / args.input.split("/")[-1], 'r')
    main(infp, args)
