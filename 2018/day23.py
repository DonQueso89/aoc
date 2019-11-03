import re
import argparse

parser = argparse.ArgumentParser(description='Solve day 23')
parser.add_argument("infile", type=str)


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


def overlap(s1, s2):
    """
    Determine whether radii of s1 and s2 overlap (whether the manhattan spheres intersect)
    """
    return manhattan_distance(s1, s2) < (s1[-1] + s2[-1])


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
    clusters = []
    for bot in nanobots:
        for _set in clusters:
            if all([overlap(bot, x) for x in _set]):
                _set.add(bot)
        clusters.append({bot})

    print(max(clusters, key=lambda k: len(k)))


if __name__ == '__main__':
    args = parser.parse_args()
    data = open(args.infile).read()
    num_in_range = num_nanobots_in_range(prep_data(data))
    print("Part 1: " + str(num_in_range))
    print("Part 2: " + str(solve(prep_data(data))))
