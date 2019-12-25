#!/usr/bin/env python

import argparse


parser = argparse.ArgumentParser()
parser.add_argument('infile', type=str)


NEW = 0
CUT = 1
INCREMENT = 2


def prep_data(blob):
    data = []
    for line in blob.splitlines():
        if 'increment' in line:
            data.append((INCREMENT, int(line.split().pop())))
        if 'cut' in line:
            data.append((CUT, int(line.split().pop())))
        if 'new stack' in line:
            data.append((NEW, 0))
    return data


def solve(instructions):
    idx = 5
    size = 10
    for func, n in instructions:
        if func == NEW:
            idx = size - idx - 1
        elif func == CUT:
            if n >= 0 and idx < n:
                idx = size - (n - idx)
            elif n >= 0 and idx >= n:
                idx -= n
            elif n < 0 and size + n < idx:
                idx = idx - (size + n)
            elif n < 0 and size + n > idx:
                idx = size - ((size + n) - idx)
        elif func == INCREMENT:
            idx += idx * n
            idx %= size
    return idx


if __name__ == '__main__':
    args = parser.parse_args()
    data = prep_data(open(args.infile).read())
    print("Part 1: {:d}".format(solve(data)))
