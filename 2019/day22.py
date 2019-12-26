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
    idx = 2019
    size = 10007
    for func, n in instructions:
        if func == NEW:
            idx = size - idx - 1
        elif func == CUT:
            split = n
            if split < 0:
                split += size
            if idx < split:
                idx = size - (split - idx)
            elif idx >= split:
                idx -= split
        elif func == INCREMENT:
            idx = idx * n
            idx %= size
    return idx


def solve2(instructions):
    idx = 2020
    size = 119315717514047
    cnt = 0
    s = set()
    while cnt < 101741582076661:
        for func, n in instructions:
            if func == NEW:
                idx = size - idx - 1
            elif func == CUT:
                split = n
                if split < 0:
                    split += size
                if idx < split:
                    idx = size - (split - idx)
                elif idx >= split:
                    idx -= split
            elif func == INCREMENT:
                idx = idx * n
                idx %= size
        if idx in s:
            s.add(idx)
            print(len(s))
        cnt += 1
    return idx


if __name__ == '__main__':
    args = parser.parse_args()
    data = prep_data(open(args.infile).read())
    print("Part 1: {:d}".format(solve(data)))
    print("Part 2: {:d}".format(solve2(data)))
