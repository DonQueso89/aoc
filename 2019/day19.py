#!/usr/bin/env python

import argparse
from day5 import prep_data, intcode_runtime
from collections import defaultdict as _dct


parser = argparse.ArgumentParser()
parser.add_argument('infile', type=str)


def solve(program):
    cnt = 0
    for y in range(50):
        line = ''
        for x in range(50):
            output, _, _, _ = intcode_runtime(
                data=_dct(int, {k: v for k, v in program.items()}),
                _inputs=[x, y],
                feedback_mode=True,
            )
            line += {1: '#', 0: '.'}[output]
            if output == 1:
                cnt += 1
        #  print(line)
    return cnt


def sides(program, i):
    """
    calculate sides for ith layer
    num touched grows slower than y, so if x == y we're searching wide enough
    return x for left and right side
    """
    left, right = None, None
    for x in range(i):
        output, _, _, _ = intcode_runtime(
            data=_dct(int, {k: v for k, v in program.items()}),
            _inputs=[x, i],
            feedback_mode=True,
        )
        if output == 1 and left is None:
            left = x
        if output == 0 and left is not None and right is None:
            right = x
    return left, right


def solve2(program):
    lower_bound = 0
    upper_bound = 1500

    while True:
        # Coarse search
        offset = (lower_bound + upper_bound) // 2
        lower_left, lower_right = sides(program, offset)
        upper_left, upper_right = sides(program, offset + 100)

        if lower_right - 100 < upper_left:
            lower_bound = offset + 1
        elif lower_right - 100 > upper_left:
            upper_bound = offset - 1
        elif lower_right - 100 == upper_left:
            # Fine search
            extra = 0
            for i in range(1, 10):
                can_go_lower = sides(program, offset - i)[1] - 100 == sides(program, offset + (100 - i))[0]
                if can_go_lower:
                    extra = i

            offset -= extra
            _, lower_right = sides(program, offset)
            return (lower_right - 102) * 10000 + (offset - 2)


if __name__ == '__main__':
    args = parser.parse_args()
    data = prep_data(open(args.infile).read())
    print("Part 1: {:d}".format(solve(data)))
    print("Part 2: {:d}".format(solve2(data)))
