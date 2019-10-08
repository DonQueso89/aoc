import re
import argparse

parser = argparse.ArgumentParser(description='Solve day 23')
parser.add_argument("infile", type=str)


def num_nanobots_in_range(nanobots):
    """
    Get the number of nanobots in range of the strongest
    nanobot.

    :param: nanobots:: [(x, y, z, r), (...), ...]

    return num_nanobots_in_range:: int
    """
    nanobots = sorted(nanobots, key=lambda k: k[3])
    sx, sy, sz, sr = nanobots.pop()
    in_range = 1
    for x, y, z, _ in nanobots:
        manhattan_distance = sum([
            abs(sx * -1 + x),
            abs(sy * -1 + y),
            abs(sz * -1 + z),
        ])
        if manhattan_distance <= sr:
            in_range += 1

    return in_range


if __name__ == '__main__':
    args = parser.parse_args()
    data = open(args.infile).read()
    nanobots = []
    for line in data.splitlines():
        nanobots.append([
            int(x) for x in re.sub(
                r'[<>r=pos]', '',
                line
            ).split(',')
        ])
    import ipdb; ipdb.set_trace();
    num_in_range = num_nanobots_in_range(nanobots)
    print("Part 1: " + str(num_in_range))
