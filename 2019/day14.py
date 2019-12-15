#!/usr/bin/env python

import argparse
import math
from collections import defaultdict
from functools import reduce


parser = argparse.ArgumentParser()
parser.add_argument('infile', type=str)


def prep_data(blob):
    reactions = {}  # (<chemical>) => (nchemical, set((<chemical>, nchemical) ...))
    for line in blob.splitlines():
        line = line.replace('>', '').split("=")
        chemical = line.pop().strip().split()
        chemical[0] = int(chemical[0])
        reaction = {(x.split()[1], int(x.split()[0])) for x in line.pop().strip().split(',')}
        reactions[chemical[1]] = (chemical[0], reaction)
    return reactions


def resolve_deps(reactions, in_leftovers=defaultdict(int)):
    required_for_fuel = defaultdict(int, reactions.pop('FUEL')[1])
    leftovers = defaultdict(int)
    while True:
        if all([x == 'ORE' for x in required_for_fuel]):
            return required_for_fuel['ORE'], leftovers

        dependencies = set()
        for g in reactions:
            for d in reactions[g][1]:
                dependencies.add(d[0])

        # Resolve chemicals only when nothing depends on them
        resolvable = [x for x in required_for_fuel if x not in dependencies and x != 'ORE']
        for chemical in resolvable:
            num_required = math.ceil(required_for_fuel.pop(chemical) - in_leftovers[chemical])
            num_producable, dependencies = reactions.pop(chemical)
            multiplier_raw = num_required / num_producable
            multiplier = math.ceil(multiplier_raw)
            excess = multiplier_raw - multiplier

            for dependency, d_required in dependencies:
                required_for_fuel[dependency] += (multiplier * d_required)
                leftovers[dependency] += (excess * d_required)


def solve(reactions):
    ore = 1000000000000
    first, leftovers = resolve_deps({k: v for k, v in reactions.items()})
    ore -= first
    fuel = 1
    while ore > 0:
        required, leftovers = resolve_deps({k: v for k, v in reactions.items()})
        ore -= required
        fuel += 1
    return first, fuel

if __name__ == '__main__':
    args = parser.parse_args()
    data = prep_data(open(args.infile).read())
    print("Part 1: {:d}\nPart 2: {:d}".format(*solve(data)))
