#!/usr/bin/env python

import argparse
from collections import defaultdict


parser = argparse.ArgumentParser()
parser.add_argument('infile', type=str)
parser.add_argument('input', type=int)


def prep_data(blob):
    memory = defaultdict(int)
    for i, x in enumerate(blob.split(',')):
            memory[i] = int(x)
    return memory


POSITION_MODE = 0
VALUE_MODE = 1
RELATIVE_MODE = 2


def resolve_inputs(modes, inputs, relative_base, data):
    resolved_inputs = []
    modes = list(str(modes))
    for i in inputs:
        mode = '0'
        try:
            mode = modes.pop()
        except IndexError:
            pass
        if mode == '0':
            resolved_inputs.append(data[i])
        elif mode == '1':
            resolved_inputs.append(i)
        elif mode == '2':
            if i + relative_base < 0:
                raise Exception("negative memoryaddress")
            resolved_inputs.append(data[i + relative_base])
        else:
            raise Exception("Unknown mode")

    resolved_inputs.append(True if modes and modes.pop() == '2' else False)
    return resolved_inputs


def intcode_runtime(data, _inputs, pointer=None, feedback_mode=False):
    _inputs = _inputs[::-1]
    diagnostic = 0
    relative_base = 0
    if pointer is None:
        pointer = 0

    while data[pointer] != 99:
        op = data[pointer]
        optype = op % 10
        if pointer < 0:
            raise Exception("Invalid pointer value")
        if optype == 1:
            a, b, o = data[pointer+1], data[pointer+2], data[pointer+3]
            op //= 100
            a, b, relative = resolve_inputs(
                modes=op,
                inputs=[a, b],
                relative_base=relative_base,
                data=data,
            )
            if relative:
                o += relative_base
            data[o] = a + b
            pointer += 4
        elif optype == 2:
            a, b, o = data[pointer+1], data[pointer+2], data[pointer+3]
            op //= 100
            a, b, relative = resolve_inputs(
                modes=op,
                inputs=[a, b],
                relative_base=relative_base,
                data=data,
            )
            if relative:
                o += relative_base
            data[o] = a * b
            pointer += 4
        elif optype == 3:
            o = data[pointer+1]
            op //= 100
            if op == 2:
                o += relative_base
            data[o] = _inputs.pop()
            pointer += 2
        elif optype == 4:
            o = data[pointer+1]
            op //= 100
            if op == 0:
                o = data[o]
            elif op == 2:
                o = data[o + relative_base]
            diagnostic = o
            pointer += 2
            if feedback_mode:
                return o, pointer, data
            print(o)
        elif optype == 5:
            a, b = data[pointer+1], data[pointer+2]
            op //= 100
            a, b, _ = resolve_inputs(
                modes=op,
                inputs=[a, b],
                relative_base=relative_base,
                data=data,
            )
            if a:
                pointer = b
            else:
                pointer += 3
        elif optype == 6:
            a, b = data[pointer+1], data[pointer+2]
            op //= 100
            a, b, _ = resolve_inputs(
                modes=op,
                inputs=[a, b],
                relative_base=relative_base,
                data=data,
            )
            if not a:
                pointer = b
            else:
                pointer += 3
        elif optype == 7:
            a, b, o = data[pointer+1], data[pointer+2], data[pointer+3]
            op //= 100
            a, b, relative = resolve_inputs(
                modes=op,
                inputs=[a, b],
                relative_base=relative_base,
                data=data,
            )
            if relative:
                o += relative_base
            if a < b:
                data[o] = 1
            else:
                data[o] = 0
            pointer += 4
        elif optype == 8:
            a, b, o = data[pointer+1], data[pointer+2], data[pointer+3]
            op //= 100
            a, b, relative = resolve_inputs(
                modes=op,
                inputs=[a, b],
                relative_base=relative_base,
                data=data,
            )
            if relative:
                o += relative_base
            if a == b:
                data[o] = 1
            else:
                data[o] = 0
            pointer += 4
        elif optype == 9:
            o = data[pointer+1]
            op //= 100
            if op == 2:
                relative_base += data[o + relative_base]
            elif op == 1:
                relative_base += o
            elif op == 0:
                relative_base += data[o]
            pointer += 2
        else:
            raise Exception("hit unknown case")

    if feedback_mode:
        return diagnostic, None, None
    return diagnostic


def solve(data, _inputs):
    return intcode_runtime(data, _inputs)


if __name__ == '__main__':
    args = parser.parse_args()
    data = prep_data(open(args.infile).read())
    print("Diagnostic: {:d}".format(solve(data, [args.input])))
