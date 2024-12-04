#!/usr/bin/env python

import argparse
from io import TextIOWrapper
from pathlib import Path

parser = argparse.ArgumentParser(description="day 12")

parser.add_argument("input", type=str, help="input file")

dir_ = Path(__file__).parent


def get_result(inp):
    result = 0
    for mask, groups in inp:
        num_bits = len(mask)
        end_bit = 1 << num_bits
        full_mask = end_bit - 1
        bit_mask = int(mask.replace("?", "0"), 2)
        non_bit_mask = int(mask.replace("?", "1"), 2) ^ full_mask

        min_bits = sum(groups) + len(groups) - 1

        offset = 0
        base = 0
        for g in reversed(groups):
            base += ((1 << g) - 1) << offset

            offset += g + 1

        def valid(bits, start, end):
            if end in [0, -1]:
                _bit_mask = int(bin(bit_mask)[2:].zfill(num_bits)[start - 1 :], 2)
                _non_bit_mask = int(
                    bin(non_bit_mask)[2:].zfill(num_bits)[start - 1 :], 2
                )
            else:
                _bit_mask = int(
                    bin(bit_mask)[2:].zfill(num_bits)[start - 1 : end + 1], 2
                )
                _non_bit_mask = int(
                    bin(non_bit_mask)[2:].zfill(num_bits)[start - 1 : end + 1], 2
                )
            if end < 0:
                bits <<= 1
            _full_mask = (1 << (end - start) + 2) - 1
            return (bits & _bit_mask) == _bit_mask and (
                (bits ^ _full_mask) & _non_bit_mask
            ) == _non_bit_mask

        def correct(test):
            _bit_mask = bit_mask
            _non_bit_mask = non_bit_mask
            return (test & _bit_mask) == _bit_mask and (
                (test ^ full_mask) & _non_bit_mask
            ) == _non_bit_mask

        def is_prefix(test):
            test_len = len(bin(test)[2:])
            _bit_mask = int(bin(bit_mask)[2:].zfill(num_bits)[-test_len:], 2)
            _non_bit_mask = int(bin(non_bit_mask)[2:].zfill(num_bits)[-test_len:], 2)
            _full_mask = (1 << test_len) - 1
            return (test & _bit_mask) == _bit_mask and (
                (test ^ _full_mask) & _non_bit_mask
            ) == _non_bit_mask

        nums = []

        offset = 0
        for g in reversed(groups):
            nums.append([])
            for i in range((num_bits - min_bits) + 1):
                n = (1 << g) - 1
                if valid(n, -(offset + i + g), -(offset + i)):
                    nums[-1].append(n << offset + i)
                else:
                    nums[-1].append(None)
            offset += g + 1

        def explore(_groups, s=0):
            if not _groups:
                return correct(s)

            #if not is_prefix(s):
                #return 0

            group = _groups.pop(0)
            _s = 0
            for i, x in enumerate(group):
                if x is None:
                    continue
                if bin((s << 1) & (x >> 1)).count("1") <= 1 and x > s:
                    _s += explore([g[i:] for g in _groups[::]], x + s)
            return _s

        result += explore(nums)
    return result


def main(infp: TextIOWrapper, args: argparse.Namespace):
    inp = [x.split() for x in infp.read().splitlines()]
    inp = [
        (
            s.replace("#", "1").replace(".", "0"),
            [int(n) for n in groups.split(",")],
        )
        for s, groups in inp
    ]

    print("result: ", get_result(inp))

    inp = [("?".join([s] * 5), groups * 5) for s, groups in inp]

    print(get_result(inp))


if __name__ == "__main__":
    args = parser.parse_args()
    infp = open(dir_ / args.input.split("/")[-1], "r")
    main(infp, args)
