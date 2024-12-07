#!/usr/bin/env python

import argparse
from io import TextIOWrapper
from pathlib import Path

parser = argparse.ArgumentParser(description='day X')

parser.add_argument('input', type=str, help='input file')

dir_ = Path(__file__).parent

def bubblesort(arr, lt):
    n = len(arr)
    while n > 0:
        for i in range(n - 1):
            if lt(arr[i], arr[i+1]):
                arr[i] += arr[i+1]
                arr[i+1] = arr[i] - arr[i+1]
                arr[i] = arr[i] - arr[i+1]
        n -= 1
    return arr


def main(infp: TextIOWrapper, args: argparse.Namespace):
    inp = infp.read().splitlines()

    parents = {}
    updates = []

    for line in inp:
        if "|" in line:
            a, b = line.split("|")
            parents.setdefault(int(a), set()).add(int(b))
        elif "," in line:
            update = [int(x) for x in line.split(",")]
            updates.append(update)
    
    def lt(a, b, _update):
        _update = set(_update)
        _parents = parents.get(a, set()) & _update
        while _parents:
            if b in _parents:
                return True
            _parents = set.union(*([parents.get(x, set()) for x in _parents])) & _update
        return False
    
    def is_sorted(_update):
        for i in range(len(_update) - 1):
            if not lt(_update[i], _update[i + 1], _update):
                return False
        return True

    s = 0
    s2 = 0
    for u in updates:
        if is_sorted(u):
            s += u[len(u) // 2]
        else:
            s2 += bubblesort(u, lambda a, b: lt(a, b, u))[len(u) // 2]
    print(s)
    print(s2)



if __name__ == '__main__':
    args = parser.parse_args()
    infp = open(dir_ / args.input.split("/")[-1], 'r')
    main(infp, args)
