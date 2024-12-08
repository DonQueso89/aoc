#!/usr/bin/env python

import argparse
from io import TextIOWrapper
from pathlib import Path

parser = argparse.ArgumentParser(description='day X')

parser.add_argument('input', type=str, help='input file')

dir_ = Path(__file__).parent

nesw = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def sim(pos, dir_, grid):
    visited = set([(pos, dir_)])
    dir_vec = nesw[dir_]
    while True:
        visited.add((pos, dir_))
        _pos = (pos[0] + dir_vec[0], pos[1] + dir_vec[1])
        if (_pos, dir_) in visited:
            return None
        try:
            e = grid[_pos]
            if e == '#':
                dir_ += 1
                dir_  %= 4
                dir_vec = nesw[dir_]
            else:
                pos = _pos
                visited.add((_pos, dir_))
        except KeyError:
            break
    return visited


def main(infp: TextIOWrapper, args: argparse.Namespace):
    inp = infp.read().splitlines()

    grid = {}
    pos = None
    dir_ = None
    for y in range(len(inp)):
        for x in range(len(inp[y])):
            e = inp[y][x]
            grid[(x, y)] = e
            if e not in ['.', '#']:
                pos = (x, y)
                dir_ = {'^': 0, '>': 1, 'v': 2, '<': 3}[e]
    
    origin = pos, dir_
    visited = sim(pos, dir_, grid)
    print(len(set([x[0] for x in visited])))

    obstructions = set()
    for pos in set([x[0] for x in visited]):
        if grid.get(pos) == '.':
            _orig_e = grid[pos]
            grid[pos] = '#'
            if sim(*origin, grid) is None:
                obstructions.add(pos)
            grid[pos] = _orig_e
    print(len(obstructions))



if __name__ == '__main__':
    args = parser.parse_args()
    infp = open(dir_ / args.input.split("/")[-1], 'r')
    main(infp, args)
