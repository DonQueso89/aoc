#!/usr/bin/env python

import argparse
from io import TextIOWrapper
from pathlib import Path

parser = argparse.ArgumentParser(description="day X")

parser.add_argument("input", type=str, help="input file")

dir_ = Path(__file__).parent


def main(infp: TextIOWrapper, args: argparse.Namespace):
    inp = infp.read()

    def parser(code, extended=False):
        i = 0
        _parsing = False
        lhs, rhs = [], []
        arg = None
        enabled = True
        while i < len(code):
            if extended and code[i : i + 7] == "don't()":
                enabled = False
                i += 7
                continue
            if extended and code[i : i + 4] == "do()":
                enabled = True
                i += 4
                continue
            elif code[i : i + 4] == "mul(":
                i += 4
                _parsing = True
                arg = lhs
                continue
            elif _parsing and code[i].isdigit():
                arg.append(int(code[i]))
            elif _parsing and code[i] == ",":
                arg = rhs
            elif _parsing and code[i] == ")":
                n1, n2 = 0, 0
                for exp in range(len(lhs)):
                    n1 += lhs[-exp - 1] * 10**exp
                for exp in range(len(rhs)):
                    n2 += rhs[-exp - 1] * 10**exp

                if enabled:
                    yield n1, n2

                lhs, rhs = [], []
                _parsing = False
            else:
                _parsing = False
                lhs, rhs = [], []
            i += 1

    s = 0
    for n1, n2 in parser(inp):
        s += n1 * n2
    print(s)

    s = 0
    for n1, n2 in parser(inp, extended=True):
        s += n1 * n2
    print(s)

if __name__ == "__main__":
    args = parser.parse_args()
    infp = open(dir_ / args.input.split("/")[-1], "r")
    main(infp, args)
