import argparse
from io import TextIOWrapper
from pathlib import Path

parser = argparse.ArgumentParser(description="day 11")

parser.add_argument("input", type=str, help="input file")

dir_ = Path(__file__).parent


def transpose(m):
    return list(map(list, zip(*m)))


def weighted_distance(galaxies, x_expansions, y_expansions, weight):
    tot_dist = 0
    _galaxies = list(galaxies)
    while _galaxies:
        cur = _galaxies.pop()
        for _other in _galaxies:
            x_start, x_end = sorted([cur[0], _other[0]])
            y_start, y_end = sorted([cur[1], _other[1]])
            for x in range(x_start, x_end):
                if x in x_expansions:
                    tot_dist += weight
                else:
                    tot_dist += 1
            for y in range(y_start, y_end):
                if y in y_expansions:
                    tot_dist += weight
                else:
                    tot_dist += 1

    return tot_dist


def main(infp: TextIOWrapper, args: argparse.Namespace):
    inp = infp.read().splitlines()
    x_expansions = set()
    y_expansions = set()

    for y, line in enumerate(inp):
        try:
            int(line.replace(".", "0"))
            y_expansions.add(y)
        except:
            pass

    inp = transpose(inp)
    for x, line in enumerate(inp):
        try:
            int("".join(line).replace(".", "0"))
            x_expansions.add(x)
        except:
            pass

    inp = transpose(inp)

    galaxies = set()
    for y, line in enumerate(inp):
        for x, char in enumerate(line):
            if char == "#":
                galaxies.add((x, y))
    print(weighted_distance(galaxies, x_expansions, y_expansions, 2))
    print(weighted_distance(galaxies, x_expansions, y_expansions, 1e6))


if __name__ == "__main__":
    args = parser.parse_args()
    infp = open(dir_ / args.input.split("/")[-1], "r")
    main(infp, args)
