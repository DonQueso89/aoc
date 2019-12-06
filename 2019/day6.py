#!/usr/bin/env python

import argparse
from collections import defaultdict


parser = argparse.ArgumentParser()
parser.add_argument('infile', type=str)


def prep_data(blob):
    # { centre: set(sattelites) }
    r = [x.split(')') for x in blob.splitlines()]
    d = defaultdict(set)
    for centre, sattelite in r:
        d[centre].add(sattelite)
    return d


def walk_orbit_tree(centre, orbit_map, depth, depths):
    depths[centre] = depth

    if centre not in orbit_map:
        return

    for sattelite in orbit_map[centre]:
        walk_orbit_tree(sattelite, orbit_map, depth + 1, depths)
    return depths


def solve(orbit_map):
    depths = {}
    walk_orbit_tree('COM', orbit_map, 0, depths)

    ancestors_me = set()
    ancestors_santa = set()
    reverse_orbit_map = {}
    for k, v in orbit_map.items():
        for s in v:
            reverse_orbit_map[s] = k

    ancestor = 'YOU'
    while ancestor in reverse_orbit_map:
        ancestor = reverse_orbit_map[ancestor]
        ancestors_me.add(ancestor)

    ancestor = 'SAN'
    while ancestor in reverse_orbit_map:
        ancestor = reverse_orbit_map[ancestor]
        ancestors_santa.add(ancestor)

    common_ancestors = ancestors_me & ancestors_santa
    closest = max(common_ancestors, key=lambda k: depths[k])
    transfer_distance = (depths['YOU'] - depths[closest]) + (depths['SAN'] - depths[closest])

    return sum(depths.values()), transfer_distance - 2  # transfer to first parent


if __name__ == '__main__':
    args = parser.parse_args()
    data = prep_data(open(args.infile).read())
    print("Part 1: {:d}\nPart 2: {:d}".format(*solve(data)))
