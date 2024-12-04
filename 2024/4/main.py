#!/usr/bin/env python

import argparse
from io import TextIOWrapper
from pathlib import Path

parser = argparse.ArgumentParser(description='day X')

parser.add_argument('input', type=str, help='input file')

dir_ = Path(__file__).parent

angles = [0, 45, 90, 135, 180, 225, 270, 315]

def rotated_vec(scale, angle):
    vec = {
        0: (1, 0),
        45: (1, 1),
        90: (0, 1),
        135: (-1, 1),
        180: (-1, 0),
        225: (-1, -1),
        270: (0, -1),
        315: (1, -1),
    }[angle]
    for y in range(*scale):
        yield (vec[0] * y, vec[1] * y)

def main(infp: TextIOWrapper, args: argparse.Namespace):
    inp = infp.read().splitlines()

    result = 0
    result2 = 0
    for y in range(len(inp)):
        for x in range(len(inp[y])):
            c = inp[y][x]
            if c == 'X':
                for a in angles:
                    try:
                        word = "".join([inp[y+_y][x+_x] for _x, _y in rotated_vec((0, 4), a) if 0 <= x+_x and 0 <= y+_y])
                        if word == "XMAS":
                            result += 1
                        
                    except IndexError:
                        continue
            
            if c == 'A':
                try:
                    mas1 = "".join(inp[y+_y][x+_x] for _x, _y in rotated_vec((-1, 2), 45) if 0 <= x+_x and 0 <= y+_y)
                    mas2 = "".join(inp[y+_y][x+_x] for _x, _y in rotated_vec((-1, 2), 135) if 0 <= x+_x and 0 <= y+_y)
                    if mas1 in ["MAS", "SAM"] and mas2 in ["MAS", "SAM"]:
                        result2 += 1
                except IndexError:
                    continue
    print(result)
    print(result2)

if __name__ == '__main__':
    args = parser.parse_args()
    infp = open(dir_ / args.input.split("/")[-1], 'r')
    main(infp, args)
