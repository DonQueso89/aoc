#!/usr/bin/env python

import argparse
from io import TextIOWrapper
from pathlib import Path
import re
import math

parser = argparse.ArgumentParser(description="day X")

parser.add_argument("input", type=str, help="input file")

dir_ = Path(__file__).parent


class System:
    def __init__(self, a1, a2, b1, b2, y1, y2):
        self.a1 = a1
        self.a2 = a2
        self.b1 = b1
        self.b2 = b2
        self.y1 = y1
        self.y2 = y2
        self.longest = max([len(str(x)) for x in [a1, a2, b1, b2, y1, y2]])
        self.solution = self._calc_echelon()

    def has_positive_integer_solution(self):
        return (
            self.solution is not None
            and math.isclose(self.solution[0], round(self.solution[0]), rel_tol=1e-13)
            and math.isclose(self.solution[1], round(self.solution[1]), rel_tol=1e-13)
            and self.solution[0] >= 0
            and self.solution[1] >= 0
        )

    def _calc_echelon(self):
        subtract = self.a2 / self.a1
        self.echelon_a2 = self.a2 - subtract * self.a1
        self.echelon_b2 = self.b2 - subtract * self.b1
        self.echelon_y2 = self.y2 - subtract * self.y1

        self.echelon_a1 = self.a1
        self.echelon_b1 = self.b1
        self.echelon_y1 = self.y1

        if self.echelon_b2 == 0:
            return None

        self.echelon_y2 = self.echelon_y2 / self.echelon_b2
        self.echelon_b2 = self.echelon_b2 / self.echelon_b2

        self.echelon_a1 = self.echelon_a1 - self.echelon_a2 * self.echelon_b1
        self.echelon_y1 = self.echelon_y1 - self.echelon_y2 * self.echelon_b1
        self.echelon_b1 = self.echelon_b1 - self.echelon_b2 * self.echelon_b1
        self.echelon_y1 = self.echelon_y1 / self.echelon_a1
        self.echelon_a1 = self.echelon_a1 / self.echelon_a1

        return self.echelon_y1, self.echelon_y2

    def get_echelon(self):
        return (
            self.echelon_a1,
            self.echelon_a2,
            self.echelon_b1,
            self.echelon_b2,
            self.echelon_y1,
            self.echelon_y2,
        )

    def print_echelon(self):
        print(self._repr(*self.get_echelon(), self.longest))

    def _repr(self, a1, a2, b1, b2, y1, y2, mx):
        return f"{a1:<{mx}} {b1:<{mx}} {y1:<{mx}}\n{a2:<{mx}} {b2:<{mx}} {y2:<{mx}}"

    def __repr__(self):
        return self._repr(
            self.a1, self.a2, self.b1, self.b2, self.y1, self.y2, self.longest
        )


def main(infp: TextIOWrapper, args: argparse.Namespace):
    inp = infp.read()

    systems = [[]]
    for line in inp.splitlines():
        if len(line) == 0:
            systems[-1] = System(*systems[-1])
            systems.append([])
        if "Button" in line:
            a1, a2 = [int(x) for x in re.findall(r"\d+", line)]
            systems[-1] += [a1, a2]
        elif "Prize" in line:
            a1, a2 = [int(x) for x in re.findall(r"\d+", line)]
            systems[-1] += [a1, a2]

    systems[-1] = System(*systems[-1])

    tokens = 0
    tokens2 = 0
    for system in systems:
        if system.has_positive_integer_solution():
            tokens += system.solution[0] * 3
            tokens += system.solution[1]
        print()

        system.y1 += 10e12
        system.y2 += 10e12
        system.solution = system._calc_echelon()
        print(system.solution)
        system.print_echelon()
        if system.has_positive_integer_solution():
            tokens2 += system.solution[0] * 3
            tokens2 += system.solution[1]
    print(tokens)
    print(tokens2)


if __name__ == "__main__":
    args = parser.parse_args()
    infp = open(dir_ / args.input.split("/")[-1], "r")
    main(infp, args)
