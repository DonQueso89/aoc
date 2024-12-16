#!/usr/bin/env python

import argparse
from itertools import chain
from io import TextIOWrapper
from pathlib import Path

parser = argparse.ArgumentParser(description='day X')

parser.add_argument('input', type=str, help='input file')

dir_ = Path(__file__).parent

def geomsum(n):
    return n * (n + 1) // 2

def checksum(inp):
    n = len(inp) - 1

    left_id = 0
    right_id = n - (n % 2)
    n_compacted = 0
    _checksum = 0
    n_compactable = 0

    while True:
        if left_id > right_id:
            return _checksum
        up_bound = (n_compacted + inp[left_id])
        if left_id % 2 == 0:
            _checksum += (left_id // 2) * (geomsum(up_bound - 1) - geomsum(max(n_compacted - 1, 0)))
            n_compacted = up_bound
            left_id += 1
        else:
            for i in range(n_compacted, up_bound):
                n_compactable = inp[right_id]
                while n_compactable == 0:
                    right_id -= 2
                    n_compactable = inp[right_id]
                if left_id > right_id:
                    return _checksum

                _checksum += i * (right_id // 2)
                inp[right_id] = n_compactable - 1
            left_id += 1
        n_compacted = up_bound

class Disk:
    def __init__(self, inp):
        self.inp = inp
        self.blocks = []
        for i, e in enumerate(inp):
            if i % 2 == 0:
                self.blocks += [i // 2] * e 
            else:
                self.blocks += [None] * e 

    def find_space(self, n, threshold):
        start, end = None, None
        for i, e in enumerate(self.blocks):
            if i > threshold:
                return None
            if e is None and start is None:
                start = i
            elif e is not None and start is not None:
                end = i
                if (end - start) >= n:
                    return (start, end)
                else:
                    start, end = None, None
    
    def compact(self):
        n = len(self.inp)
        right_id = n - (n % 2)
        while right_id > 0:
            num_compactable = self.inp[right_id]
            low_bound = sum(self.inp[:right_id])
            up_bound = low_bound + num_compactable
            gap = self.find_space(num_compactable, low_bound)
            if gap is not None:
                start, end = gap
                for i in range(start, start + num_compactable):
                    self.blocks[i] = (right_id // 2)
                for i in range(low_bound, up_bound):
                    self.blocks[i] = None
            right_id -= 2
    
    def print_blocks(self):
        print("".join([str(x) if x is not None else "." for x in self.blocks]))
    
    def checksum(self):
        _checksum = 0
        for i, e in enumerate(self.blocks):
            if e is not None:
                _checksum += i * e
        return _checksum

def main(infp: TextIOWrapper, args: argparse.Namespace):
    inp = [int(x) for x in infp.read()]
    print(checksum(inp[::]))
    disk = Disk(inp)
    disk.compact()
    print(disk.checksum())

if __name__ == '__main__':
    args = parser.parse_args()
    infp = open(dir_ / args.input.split("/")[-1], 'r')
    main(infp, args)
