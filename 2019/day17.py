#!/usr/bin/env python

import argparse
from day5 import prep_data, intcode_runtime
from cytoolz import partition_all
from collections import Counter


parser = argparse.ArgumentParser()
parser.add_argument('infile', type=str)


def solve(program):
    output = 35
    pointer = 0
    relative_base = 0
    image = ""
    _program = {k:v for k,v in program.items()}
    while output in (35, 10, 46, 94):
        output, pointer, _program, relative_base = intcode_runtime(
            _program,
            _inputs=[],
            pointer=pointer,
            relative_base=relative_base,
            feedback_mode=True
        )

        if output in (35, 10, 46, 94):
            image += chr(output)

    image = [l for l in image.splitlines() if l]
    intersections = set()
    for y, line in enumerate(image):
        for x, c in enumerate(line):
            if c == '^':
                start = (x, y)
            if c == '#':
                try:
                    for (nx, ny) in [
                        (x - 1, y),
                        (x + 1, y),
                        (x, y - 1),
                        (x, y + 1),
                    ]:
                        assert image[ny][nx] == '#'
                    intersections.add((x, y))
                except (IndexError, AssertionError):
                    continue

    dirs = 'NESW'
    max_y, max_x = len(image), len(image[0])

    def turn(_x, _y, _dir):
        if _dir in (0, 2):
            if _x - 1 >= 0 and image[_y][_x - 1] == '#':
                next_dir = 'W'
            elif _x + 1 < max_x and image[_y][_x + 1] == '#':
                next_dir = 'E'
            else:
                return None
        elif _dir in (1, 3):
            if _y - 1 >= 0 and image[_y - 1][_x] == '#':
                next_dir = 'N'
            elif _y + 1 < max_y and image[_y + 1][_x] == '#':
                next_dir = 'S'
            else:
                return None

        return {
            ('N', 'E'): 'R',
            ('N', 'W'): 'L',
            ('S', 'W'): 'R',
            ('S', 'E'): 'L',
            ('W', 'N'): 'R',
            ('W', 'S'): 'L',
            ('E', 'N'): 'L',
            ('E', 'S'): 'R',
        }[(dirs[_dir], next_dir)]

    direction = 0
    path = []
    x, y = start
    steps = 0
    while True:
        ny, nx = {
            'N': (y - 1, x),
            'S': (y + 1, x),
            'W': (y, x - 1),
            'E': (y, x + 1),
        }[dirs[direction]]

        if 0 <= nx < max_x and 0 <= ny < max_y and image[ny][nx] == '#':
            steps += 1
            x, y = nx, ny
        else:
            _turn = turn(x, y, direction)
            if _turn is None:
                break

            if steps:
                path.append(steps)
            path.append(_turn)
            steps = 0
            direction += {'L': -1, 'R': 1}[_turn]
            direction %= 4

    path.append(steps)

    A = ['L', 9, 3, 'L', 9, 3, 'L', 6, 'L', 6]
    B = ['L', 9, 3, 'L', 6, 'R', 9, 3, 'R', 8]
    C = ['R', 8, 'R', 4, 'L', 9, 3]

    func_calls = []

    i = 0
    while i < len(path):
        if path[i:i+8] == ['L', 12, 'L', 12, 'L', 6, 'L', 6]:
            func_calls.append('A')
            i += 8
        elif path[i:i+8] == ['L', 12, 'L', 6, 'R', 12, 'R', 8]:
            func_calls.append('B')
            i += 8
        elif path[i:i+6] == ['R', 8, 'R', 4, 'L', 12]:
            func_calls.append('C')
            i += 6

    main_routine = ','.join(func_calls) + '\n'
    A = list(sum(list(zip(A, [','] * len(A))), ()))
    B = list(sum(list(zip(B, [','] * len(B))), ()))
    C = list(sum(list(zip(C, [','] * len(C))), ()))
    A.pop()
    B.pop()
    C.pop()
    A += ['\n']
    B += ['\n']
    C += ['\n']
    print(main_routine)

    program[0] = 2
    pointer, relative_base = 0, 0

    line = ''
    output = -1
    inp = input()
    inp = inp.split(',')
    inp = [x for x in inp if x]
    while pointer is not None:
        if output == 10:
            print(line)
            if 'Function' in line:
                inp = input()
                inp = {'A': A, 'B': B, 'C': C}[inp]
                inp = [ord(x) if isinstance(x, str) else ord(str(x)) for x in inp]
                output, pointer, program, relative_base = intcode_runtime(
                    data=program,
                    _inputs=inp,
                    pointer=pointer,
                    relative_base=relative_base,
                    feedback_mode=True
                )
            elif 'Main' in line:
                inp = input()
                inp = inp.split(',')
                inp = [x for x in inp if x]
                inp = ",".join(map(str, inp)) + '\n'
                inp = [ord(x) for x in inp]
                output, pointer, program, relative_base = intcode_runtime(
                    data=program,
                    _inputs=inp,
                    pointer=pointer,
                    relative_base=relative_base,
                    feedback_mode=True
                )
            line = ''
            line += chr(output)
        elif output > 256:
            break
        output, pointer, program, relative_base = intcode_runtime(
            data=program,
            _inputs=[110, 10],
            pointer=pointer,
            relative_base=relative_base,
            feedback_mode=True
        )
        line += chr(output)

    return sum([x * y for x, y in intersections]), output


if __name__ == '__main__':
    args = parser.parse_args()
    data = prep_data(open(args.infile).read())
    print("Part 1: {:d}\nPart 2: {:d}".format(*solve(data)))
