#!/usr/bin/env python
import re
import argparse
from collections import defaultdict

parser = argparse.ArgumentParser(description='Solve day 23')
parser.add_argument("infile", type=str)


def _num_in_range(c, nanobots):
    in_range = 0
    for n in nanobots:
        distance = manhattan_distance(c, n)
        if distance <= n[-1]:
            in_range += 1
    return in_range
    

def manhattan_distance(s1, s2):
    return sum([
        abs(s1[0] * -1 + s2[0]),
        abs(s1[1] * -1 + s2[1]),
        abs(s1[2] * -1 + s2[2]),
    ])


def num_nanobots_in_range(nanobots):
    """
    Get the number of nanobots in range of the strongest
    nanobot.

    :param: nanobots:: [(x, y, z, r), (...), ...]

    return num_nanobots_in_range:: int
    """
    nanobots = sorted(nanobots, key=lambda k: k[3])
    strongest = nanobots.pop()
    in_range = 1
    for n in nanobots:
        distance = manhattan_distance(strongest, n)
        if distance <= strongest[-1]:
            in_range += 1
    return in_range


def cache(func):
    def wrapper(s1, s2):
        c = wrapper.cached.get((s1, s2))
        if c:
            return c
        c = func(s1, s2)
        wrapper.cached[(s1, s2)] = c
        return c
    wrapper.cached = {}
    return wrapper


@cache
def overlap(s1, s2):
    """
    Determine whether radii of s1 and s2 overlap (whether the taxicab spheres intersect)
    """
    return manhattan_distance(s1, s2) <= (s1[-1] + s2[-1])



def prep_data(data):
    nanobots = []
    for line in data.splitlines():
        nanobots.append(tuple([
            int(x) for x in re.sub(
                r'[<>r=pos]', '',
                line
            ).split(',')
        ]))
    return nanobots


def solve(nanobots):
    # Whenever each pair in a collection of these circles has a nonempty intersection, there exists an intersection point for the whole collection;
    # search coordinate space of bot with smallest radius in maximum overlapping set
    # Take the one closest to 0, 0

    # Find largest cluster of bots in with an all-2-all overlap
    # ~500000 cmps for getting per bot overlap state (sum(range(1000)) == 499500)
    # compare each set with eachother (same story)
    per_bot_overlap = defaultdict(set)
    nanobots = sorted(nanobots)
    ith_done = 0  # already matched the ones before this
    for bot1 in nanobots:
        for bot2 in nanobots[ith_done:]:
            if overlap(bot1, bot2):
                per_bot_overlap[bot1].add(bot2)
                per_bot_overlap[bot2].add(bot1)
        ith_done += 1

    per_bot_cluster = defaultdict(set)
    for bot1, cluster1 in per_bot_overlap.items():
        # bootstrap all clusters with the reference bot
        per_bot_cluster[bot1].add(bot1)
        for bot2, cluster2 in per_bot_overlap.items():
            if len(per_bot_overlap[bot1] & per_bot_overlap[bot2]) == len(per_bot_overlap[bot1]):
                per_bot_cluster[bot1].add(bot2)

    biggest_cluster_size = len(max(per_bot_cluster.values(), key=lambda k: len(k)))
    searchsize = 1
    x, y, z = (0, 0, 0)
    while True:
        searchrange = range(searchsize // 2 * -1, searchsize // 2)
        for x_offset in searchrange:
            for y_offset in searchrange:
                for z_offset in searchrange:
                    c = (x + x_offset, y + y_offset, z + z_offset, 0)
                    if _num_in_range(c, nanobots) == biggest_cluster_size:
                        return c
        searchsize += 2
        print("sweeping offsets {:d}".format(searchsize))


if __name__ == '__main__':
    args = parser.parse_args()
    data = open(args.infile).read()
    num_in_range = num_nanobots_in_range(prep_data(data))
    print("Part 1: " + str(num_in_range))
    print("Part 2: " + str(solve(prep_data(data))))
