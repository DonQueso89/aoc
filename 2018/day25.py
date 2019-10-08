import argparse

parser = argparse.ArgumentParser(description='Solve day 25')
parser.add_argument("infile", type=str)


def prep_input(fname):
    return [[int(y) for y in x.split(',')] for x in open(fname).read().splitlines()]


def manhattan_distance(p1, p2):
    return sum([
        abs(p1[0] * -1 + p2[0]),
        abs(p1[1] * -1 + p2[1]),
        abs(p1[2] * -1 + p2[2]),
        abs(p1[3] * -1 + p2[3]),
    ])


def new_constellations(point, constellations):
    """
    Given a point and some constellations, find all constellations it belongs
    to. If it belongs to multiple, it connects them.

    Return these constellations merged into one and all other constellations.
    return: 2d list
    """
    belongs = [point]  # 2d list:: 1 constellation
    does_not_belong = []   # 3d list:: a list of constellations
    for constellation in constellations:
        if any([manhattan_distance(x, point) <= 3 for x in constellation]):
            belongs.extend(constellation)
        else:
            does_not_belong.append(constellation)

    return [belongs] + does_not_belong


def solve(points):
    constellations = [[points[0]]]
    for point in points[1:]:
        constellations = new_constellations(point, constellations)
    return len(constellations)


if __name__ == '__main__':
    args = parser.parse_args()
    print("Part 1: " + str(solve(prep_input(args.infile))))
