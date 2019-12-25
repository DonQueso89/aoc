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
    idxs = list(range(10007))
    l = 10007
    for func, n in instructions:
        if func == NEW:
            idxs = idxs[::-1]
        elif func == CUT:
            idxs = idxs[n:] + idxs[:n]
        elif func == INCREMENT:
            _idxs = [None] * 10007
            i = 0
            for x in idxs:
                _idxs[i] = x
                i += n
                i %= l
            idxs = _idxs
    return idxs.index(2019)


if __name__ == '__main__':
    args = parser.parse_args()
    data = prep_data(open(args.infile).read())
    print("Part 1: {:d}".format(solve(data)))
