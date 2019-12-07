#!/usr/bin/env python

import argparse


parser = argparse.ArgumentParser()
parser.add_argument('infile', type=str)
parser.add_argument('input', type=int)


def prep_data(blob):
    return [int(x) for x in blob.split(',')]


def intcode_runtime(data, _inputs, pointer, feedback_mode):
    _inputs = _inputs[::-1]
    diagnostic = 0
    while data[pointer] != 99:
        op = data[pointer]
        optype = op % 10
        if optype == 1:
            a, b, o = data[pointer+1:pointer+4]
            op -= optype
            op = int(str(op), 2)
            op >>= 2
            if not op & 1:
                a = data[a]
            if not (op >> 1) & 1:
                b = data[b]
            data[o] = a + b
            pointer += 4
        elif optype == 2:
            a, b, o = data[pointer+1:pointer+4]
            op -= optype
            op = int(str(op), 2)
            op >>= 2
            if not op & 1:
                a = data[a]
            if not (op >> 1) & 1:
                b = data[b]
            data[o] = a * b
            pointer += 4
        elif optype == 3:
            o = data[pointer+1]
            data[o] = _inputs.pop()
            pointer += 2
        elif optype == 4:
            o = data[pointer+1]
            op -= optype
            op = int(str(op), 2)
            op >>= 2
            if not op & 1:
                o = data[o]
            diagnostic = o
            pointer += 2
            if feedback_mode:
                return o, pointer, data
        elif optype == 5:
            a, b = data[pointer+1:pointer+3]
            op -= optype
            op = int(str(op), 2)
            op >>= 2
            if not op & 1:
                a = data[a]
            if not (op >> 1) & 1:
                b = data[b]
            if a:
                pointer = b
            else:
                pointer += 3
        elif optype == 6:
            a, b = data[pointer+1:pointer+3]
            op -= optype
            op = int(str(op), 2)
            op >>= 2
            if not op & 1:
                a = data[a]
            if not (op >> 1) & 1:
                b = data[b]
            if not a:
                pointer = b
            else:
                pointer += 3
        elif optype == 7:
            a, b, o = data[pointer+1:pointer+4]
            op -= optype
            op = int(str(op), 2)
            op >>= 2
            if not op & 1:
                a = data[a]
            if not (op >> 1) & 1:
                b = data[b]
            if a < b:
                data[o] = 1
            else:
                data[o] = 0
            pointer += 4
        elif optype == 8:
            a, b, o = data[pointer+1:pointer+4]
            op -= optype
            op = int(str(op), 2)
            op >>= 2
            if not op & 1:
                a = data[a]
            if not (op >> 1) & 1:
                b = data[b]
            if a == b:
                data[o] = 1
            else:
                data[o] = 0
            pointer += 4
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
