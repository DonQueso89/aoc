#!/usr/bin/env python
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("insequence", type=str)
parser.add_argument("disksize", type=int)


def solve(insequence, disksize):
    a = int(insequence, 2)
    b = a
    num_bits = len(insequence)
    while num_bits < disksize:
        b = sum([1 << (num_bits - i - 1) for i in range(num_bits) if b >> i & 1])

        b ^= int("1" * num_bits, 2)
        a = a << (num_bits + 1)
        a += b
        b = a
        num_bits = num_bits * 2 + 1

    checksum = b
    if num_bits > disksize:
        checksum >>= (num_bits - disksize)
        num_bits = disksize

    while num_bits % 2 == 0:
        new_checksum = 0
        for i in range(0, num_bits, 2):
            mask = 0b11 << (num_bits - 2 - i)
            if checksum & mask == mask or (checksum ^ int("1" * num_bits, 2)) & mask == mask:
                new_checksum |= (1 << (i // 2))
        checksum = new_checksum
        num_bits //= 2
    return "{:0{num_bits}b}".format(checksum, num_bits=num_bits)


if __name__ == '__main__':
    args = parser.parse_args()
    print("Part 1: {}".format(solve(args.insequence, args.disksize)))
