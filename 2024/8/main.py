#!/usr/bin/env python

import argparse
from io import TextIOWrapper
from pathlib import Path

parser = argparse.ArgumentParser(description='day X')

parser.add_argument('input', type=str, help='input file')

dir_ = Path(__file__).parent

def main(infp: TextIOWrapper, args: argparse.Namespace):
    inp = infp.read().splitlines()

    antennas = {}
    for y in range(len(inp)):
        for x in range(len(inp[y])):
            if (e := inp[y][x]) != ".":
                antennas.setdefault(e, []).append((x, y))
        inp[y] = list(inp[y])
    
    antinodes = set()
    antinodes2 = set()
    for arr in antennas.values():
        antinodes2 = antinodes2 | set(arr)
        for i in range(len(arr) - 1):
            for j in range(i + 1, len(arr)):
                ax, ay, bx, by = (*arr[i], *arr[j])
                dx, dy = bx - ax, by - ay
                n = 1
                while True:
                    a, b = False, False
                    bx, by = bx + dx, by + dy
                    ax, ay = ax - dx, ay - dy
                    if 0 <= bx <= x and 0 <= by <= y:
                        b = True
                        if n == 1:
                            antinodes.add((bx, by))
                        else:
                            antinodes2.add((bx, by))
                    if 0 <= ax <= x and 0 <= ay <= y:
                        a = True
                        if n == 1:
                            antinodes.add((ax, ay))
                        else:
                            antinodes2.add((ax, ay))
                    if not a and not b:
                        break
                    n += 1
    print(len(antinodes))
    print(len(antinodes | antinodes2 | set([])))

if __name__ == '__main__':
    args = parser.parse_args()
    infp = open(dir_ / args.input.split("/")[-1], 'r')
    main(infp, args)
