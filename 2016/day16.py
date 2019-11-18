#!/usr/bin/env python
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("day", type=int)
parser.add_argument("insequence", type=str)
parser.add_argument("disksize", type=int)


def reverse_bits(n, num_bits):
    return sum([1 << (num_bits - i - 1) for i in range(num_bits) if n >> i & 1])


def simplify_checksum(checksum, num_bits):
    new_checksum = 0
    for i in range(0, num_bits, 2):
        mask = 0b11 << (num_bits - 2 - i)
        if checksum & mask == mask or (checksum ^ int("1" * num_bits, 2)) & mask == mask:
            new_checksum |= (1 << (i // 2))
    return new_checksum


def merge_checksums(checksum):
    r = checksum[0][0]
    for p, n in checksum[1:]:
        r <<= n
        r |= p
    return r


def solve(insequence, disksize):
    a = int(insequence, 2)
    b = a
    num_bits = len(insequence)
    while num_bits < disksize:
        b = reverse_bits(b, num_bits)
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
        checksum = simplify_checksum(checksum, num_bits)
        num_bits //= 2
    return "{:0{num_bits}b}".format(checksum, num_bits=num_bits)


def solve2(insequence, disksize):
    num_bits = len(insequence)
    a = [(int(insequence, 2), num_bits)]
    b = a.copy()
    while num_bits < disksize:
        b = [(reverse_bits(x, _), _) for x, _ in reversed(b)]
        b = [(x ^ int("1" * _, 2), _) for x, _ in b]
        a[-1] = (a[-1][0] << 1, a[-1][1] + 1)
        a += b
        b = [x for x in a]
        num_bits = num_bits * 2 + 1

    checksum = b
    if num_bits > disksize:
        while num_bits > disksize:
            partial_checksum, nbits = checksum.pop()
            if num_bits - checksum[-1][1] > disksize:
                num_bits -= nbits
            else:
                n_to_drop = (num_bits - disksize)
                checksum.append((partial_checksum >> n_to_drop, nbits - n_to_drop))
                num_bits -= n_to_drop

    # ensure all partial checksums are of even length
    i = 0
    while i < len(checksum):
        p, n = checksum[i]
        if n % 2 == 1:
            # take bit from the next one
            next_p, next_n = checksum[i + 1]
            p <<= 1
            p |= (next_p >> (next_n - 1))
            checksum[i] = (p, n + 1)
            checksum[i + 1] = (p ^ (p & 1 << next_n - 1), next_n - 1)
        i += 1

    # group bits into larger buckets
    grouped_checksum = []
    for i in range(0, len(checksum), 1000):
        p, n = checksum[i]
        for next_p, next_n in checksum[i + 1: i + 1000]:
            p <<= next_n
            p |= next_p
            n += next_n
        grouped_checksum.append((p, n))
    checksum = grouped_checksum

    print("Starting simplification")
    while num_bits % 2 == 0:
        if isinstance(checksum, list):
            checksum = [(simplify_checksum(x, n), n // 2) for x, n in checksum]
            if checksum[0][1] <= 50:
                # reduce back to single number
                print("continuing with a single number")
                checksum = merge_checksums(checksum)
        else:
            checksum = simplify_checksum(checksum, num_bits)
        print("simplification at {:d}".format(num_bits // 2))
        num_bits //= 2

    return "{:0{num_bits}b}".format(checksum, num_bits=nbits)


if __name__ == '__main__':
    args = parser.parse_args()
    inseq, size = args.insequence, args.disksize
    print("Part {:d}: {}".format(
        args.day,
        {
            1: lambda: solve(inseq, size),
            2: lambda: solve2(inseq, size)
        }[args.day]()
    ))
