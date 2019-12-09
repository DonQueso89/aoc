#!/usr/bin/env python

import argparse
from day5 import prep_data, intcode_runtime


parser = argparse.ArgumentParser()
parser.add_argument('infile', type=str)
parser.add_argument('input', type=int)


def solve(program, _input):
    return intcode_runtime(program, [_input])


if __name__ == '__main__':
    args = parser.parse_args()
    data = prep_data(open(args.infile).read())
    print("Part 1: {:d}".format(solve(data, args.input)))
