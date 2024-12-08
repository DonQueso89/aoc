#!/usr/bin/env python

import argparse
from io import TextIOWrapper
from pathlib import Path

parser = argparse.ArgumentParser(description='day X')

parser.add_argument('input', type=str, help='input file')

dir_ = Path(__file__).parent

def main(infp: TextIOWrapper, args: argparse.Namespace):
    inp = infp.read().splitlines()

    s = 0
    for line in inp:
        rhs, lhs = line.split(":")
        rhs = int(rhs)
        lhs = [int(x.strip()) for x in lhs.split()]
        candidates = [lhs[0]]
        for l in lhs[1:]:
            _candidates = []
            for c in candidates:
                _candidates.append(c + l)
                _candidates.append(c * l)
                _candidates.append(int(str(c) + str(l)))
            candidates = _candidates
        if rhs in candidates:
            s += rhs
    print(s)

            



if __name__ == '__main__':
    args = parser.parse_args()
    infp = open(dir_ / args.input.split("/")[-1], 'r')
    main(infp, args)
