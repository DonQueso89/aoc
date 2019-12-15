#!/usr/bin/env python

import argparse
import math
from collections import defaultdict


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


def resolve_deps(reactions, fuel_required=1):
    required_for_fuel = defaultdict(int, reactions.pop('FUEL')[1])
    required_for_fuel = defaultdict(int, {k: v * fuel_required for k, v in required_for_fuel.items()})
    while True:
        if all([x == 'ORE' for x in required_for_fuel]):
            return required_for_fuel['ORE']

        dependencies = set()
        for g in reactions:
            for d in reactions[g][1]:
                dependencies.add(d[0])

        # Resolve chemicals only when nothing depends on them
        resolvable = [x for x in required_for_fuel if x not in dependencies and x != 'ORE']

        for chemical in resolvable:
            num_required = math.ceil(required_for_fuel.pop(chemical))
            num_producable, dependencies = reactions.pop(chemical)
            multiplier = math.ceil(num_required / num_producable)

            for dependency, d_required in dependencies:
                required_for_fuel[dependency] += (multiplier * d_required)


def solve(reactions):
    def reactory():
        return {k: v for k, v in reactions.items()}
    single_fuel = resolve_deps(reactory())
    ore_available = 1000000000000
    lower_bound, upper_bound = 0, ore_available
    while True:
        num_fuel = (upper_bound + lower_bound) // 2
        ore_required = resolve_deps(reactory(), num_fuel)

        if ore_required == ore_available:
            return single_fuel, num_fuel

        if ore_required < ore_available:
            if resolve_deps(reactory(), num_fuel + 1) >= ore_available:
                return single_fuel, num_fuel
            lower_bound = num_fuel
        elif ore_required > ore_available:
            if resolve_deps(reactory(), num_fuel - 1) <= ore_available:
                return single_fuel, num_fuel - 1
            upper_bound = num_fuel


if __name__ == '__main__':
    args = parser.parse_args()
    data = prep_data(open(args.infile).read())
    print("Part 1: {:d}\nPart 2: {:d}".format(*solve(data)))
