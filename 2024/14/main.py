#!/usr/bin/env python

import argparse
from io import TextIOWrapper
from pathlib import Path
import re

parser = argparse.ArgumentParser(description='day X')

parser.add_argument('input', type=str, help='input file')

dir_ = Path(__file__).parent

def probable_egg(robots):
    n = len(robots)
    robots = {(x, y) for x, y, _, _ in robots}
    n_adjacent = 0
    for x, y in robots:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == dy == 0:
                    continue
                if (x + dx, y + dy) in robots:
                    n_adjacent += 1
            if n_adjacent >= n:
                return True
    return False

def print_grid(robots, xlim, ylim):
    robots = {(x, y) for x, y, _, _ in robots}
    for y in range(ylim):
        l = ""
        for x in range(xlim):
            if (x, y) in robots:
                l += "#"
            else:
                l += "."
        print(l)

def main(infp: TextIOWrapper, args: argparse.Namespace):
    inp = infp.read()
    
    xlim, ylim = 101, 103  # 11, 7
    robots = []
    for line in inp.split('\n'):
        if not line:
            continue
        x, y, vx, vy = map(int, re.findall(r'-?\d+', line))
        robots.append([x, y, vx, vy])
    secs = 0
    while True:
        for i  in range(len(robots)):
            x, y, vx, vy = robots[i]
            x, y = x + vx, y + vy
            if x >= xlim:
                x = (x - xlim)
            if x < 0:
                x = (x + xlim)
            if y >= ylim:
                y = (y - ylim)
            if y < 0:
                y = (y + ylim)
            
            robots[i][0] =  x
            robots[i][1] =  y
        secs += 1

        if probable_egg(robots):
            print_grid(robots, xlim, ylim)
            print(secs)

    coeffs = [0, 0, 0, 0]
    _robots = [(x, y) for x, y, _, _ in robots]
    while _robots:
        x, y = _robots.pop()
        if 0 <= x < xlim // 2 and 0 <= y < ylim // 2:
            coeffs[0] += 1
        elif 0 <= x < xlim // 2 and y > ylim // 2:
            coeffs[1] += 1
        elif x > xlim // 2 and y > ylim // 2:
            coeffs[2] += 1
        elif x > xlim // 2 and 0 <= y < ylim // 2:
            coeffs[3] += 1
    print(coeffs)
    print(coeffs[0] * coeffs[1] * coeffs[2] * coeffs[3])

    


if __name__ == '__main__':
    args = parser.parse_args()
    infp = open(dir_ / args.input.split("/")[-1], 'r')
    main(infp, args)
