#!/usr/bin/env python

import argparse
from io import TextIOWrapper
from pathlib import Path

parser = argparse.ArgumentParser(description='day X')

parser.add_argument('input', type=str, help='input file')

dir_ = Path(__file__).parent

def num_safe(inp):
    safe = 0
    leftover = []
    for numbers in inp:
        orig = numbers[::]

        sign = None
        while len(numbers) > 1:
            n = numbers.pop()
            delta = numbers[-1] - n
            if sign is None:
                sign = delta < 0
            
            if not abs(delta) > 0 or not abs(delta) < 4 or (delta < 0) != sign:
                leftover.append(orig)
                break
        else:
            safe += 1
    return safe, leftover

def main(infp: TextIOWrapper, args: argparse.Namespace):
    inp = infp.read().splitlines()
    inp = [list(map(int, line.split())) for line in inp]
    r1, leftover = num_safe([x[::] for x in inp])
    print(r1)
    for line in leftover:
        for i in range(len(line)):
            _mod = line[::]
            _mod.pop(i)
            _safe, _ = num_safe([_mod])
            if _safe:
                r1 += 1
                break
    print(r1)






                
                
                







if __name__ == '__main__':
    args = parser.parse_args()
    infp = open(dir_ / args.input.split("/")[-1], 'r')
    main(infp, args)
