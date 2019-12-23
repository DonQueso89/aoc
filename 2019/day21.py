#!/usr/bin/env python

import argparse
from day5 import prep_data, intcode_runtime


parser = argparse.ArgumentParser()
parser.add_argument('infile', type=str)


def solve(program):
    """
    Part 1 Springscript:
    NOT A T
    OR T J
    NOT B T
    OR T J
    NOT C T
    OR T J
    AND D J
    WALK

    Part 2 Springscript:

    NOT A T
    OR T J
    NOT B T
    OR T J
    NOT C T
    OR T J
    AND D J
    AND E T
    OR H T
    AND T J
    RUN
    """
    ptr, rb = 0, 0
    inputs = []
    prompt = ''
    while True:
        output, ptr, program, rb = intcode_runtime(
            data=program,
            _inputs=inputs,
            pointer=ptr,
            relative_base=rb,
            feedback_mode=True
        )

        if 0 < output < 128:
            prompt += chr(output)
        elif output > 128:
            break

        if prompt == 'Input instructions:':
            print(prompt)
            inputs = []
            while True:
                inp = input("WALK/RUN = end input\n" if not inputs else '')
                for c in inp:
                    inputs.append(ord(c))
                inputs.append(10)
                if inp in ('WALK', 'RUN'):
                    break

            prompt = ''
        elif output == 10:
            print(prompt)
            prompt = ''
    return output


if __name__ == '__main__':
    args = parser.parse_args()
    data = prep_data(open(args.infile).read())
    print("Part 1: {:d}".format(solve(data)))
