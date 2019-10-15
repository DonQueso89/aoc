import random
import re
import argparse
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument("infile", type=str)


def prep_data(blob):
    mapping = defaultdict(list)
    for line in blob.splitlines():
        if "=>" in line:
            k, v = line.split("=>")
            mapping[k.strip()].append(v.strip())
        elif line:
            startmolecule = line
    return startmolecule, mapping


def solve1(startmolecule, mapping):
    molecules = set([])
    for search, replacements in mapping.items():
        for match in re.finditer(search, startmolecule):
            start, end = match.span()
            for replacement in replacements:
                molecules.add(startmolecule[:start] + replacement + startmolecule[end:])
    return len(molecules)


MAX_DEPTH = 250
MEMOIZED = set()


def solve2(current_molecule, mapping, depth=0, desired_molecule="e"):
    probe_result = None
    if current_molecule == desired_molecule:
        return depth
    if depth == MAX_DEPTH:
        return None
    if current_molecule in MEMOIZED:
        return None
    else:
        MEMOIZED.add(current_molecule)

    new_molecules = set()
    for search, replacements in mapping.items():
        for match in re.finditer(search, current_molecule):
            start, end = match.span()
            for replacement in replacements:
                new_molecules.add(current_molecule[:start] + replacement + current_molecule[end:])
    for new_molecule in sorted(new_molecules - MEMOIZED, key=lambda k: len(k)):
        # Give preference to smallest molecule
        probe_result = solve2(
            new_molecule,
            mapping,
            depth + 1,
        )

        if probe_result is not None:
            return probe_result
    return probe_result


if __name__ == '__main__':
    args = parser.parse_args()
    print("Part 1: ", str(solve1(*prep_data((open(args.infile).read())))))
    current_molecule, mapping = prep_data((open(args.infile).read()))

    # Going from the output to the input provides a boundary for the search depth
    reversed_mapping = defaultdict(list)
    for k, v in mapping.items():
        for sv in v:
            reversed_mapping[sv].append(k)
    mapping = reversed_mapping
    print("Part 2: ", str(solve2(current_molecule, mapping)))
