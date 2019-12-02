#!/usr/bin/env python

import argparse


parser = argparse.ArgumentParser()
parser.add_argument('infile', type=str)


def prep_data(blob):
    return [int(x) for x in blob.split(',')]


def solve(data, noun, verb):
    i, op = 0, 0
    data = [x for x in data]
    data[1] = noun
    data[2] = verb
    while True:
        try:
            op, a, b, o = data[i:i+4]
            assert not op == 99
            data[o] = {
                1: lambda _a, _b: _a + _b,
                2: lambda _a, _b: _a * _b
            }[op](data[a], data[b])
        except (ValueError, AssertionError):
            break
        except KeyError:
            pass
        i += 4
    return data


def solve2(data):
    for noun in range(0, 100):
        for verb in range(0, 100):
            r = solve(data, noun, verb)
            if r[0] == 19690720:
                return "%02d" % r[1] + "%02d" % r[2]


if __name__ == '__main__':
    args = parser.parse_args()
    data = prep_data(open(args.infile).read())
    print("Part 1: {:d}".format(solve(data, 12, 2)[0]))
    print("Part 2: {}".format(solve2(data)))
