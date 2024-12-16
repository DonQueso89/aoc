#!/usr/bin/env python

import argparse
from io import TextIOWrapper
from pathlib import Path
from functools import lru_cache

parser = argparse.ArgumentParser(description="day X")

parser.add_argument("input", type=str, help="input file")

dir_ = Path(__file__).parent


class Stone:
    def __init__(self, v, left):
        self.v = v
        self.left = left

    def __str__(self):
        return f"{self.left}<-{self.v}"

def num_stones(stone, n, cache):
    if n == 0:
        return 1
    elif (stone, n) in cache:
        return cache[(stone, n)]

    if stone == 0:
        num = num_stones(1, n-1, cache)
        cache[(1, n-1)] = num
        return num
    elif (sl := len(str(stone))) % 2 == 0:
        sv = str(stone)
        a1 = int(sv[:(sl // 2)])
        a2 = int(sv[(sl // 2):])
        n1, n2 = num_stones(a1, n-1, cache), num_stones(a2, n-1, cache)
        cache[(a1, n-1)] = n1
        cache[(a2, n-1)] = n2
        return n1 + n2
    else:
        num = num_stones(stone * 2024, n-1, cache)
        cache[(stone * 2024, n-1)] = num
        return num


def main(infp: TextIOWrapper, args: argparse.Namespace):
    inp = [int(x) for x in infp.read().split()]
    n = 0
    cache = {}
    for i in inp:
        n += num_stones(i, 75, cache)
    print(n)


if __name__ == "__main__":
    args = parser.parse_args()
    infp = open(dir_ / args.input.split("/")[-1], "r")
    main(infp, args)
