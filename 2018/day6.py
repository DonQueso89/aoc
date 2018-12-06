import sys


def man_distance(a, b):
    ya, xa = a
    yb, xb = b
    return abs(ya - yb) + abs(xa - xb)


def solve(coordinates, dist_limit, gridwalker):
    infinite_grids = set()
    region_near = 0
    for coordinate in gridwalker:
        y, x = coordinate
        infinite = y == max_y or y == 0 or x == max_x or x == 0
        distances = sorted([(c, man_distance(c, coordinate)) for c in coordinates], key=lambda k: k[1])
        sum_dist = sum([d for c, d in distances])
        if sum_dist < dist_limit:
            region_near  += 1
        if coordinate in coordinates:
            coordinates[coordinate] += 1
            continue
        closest = [c for c, d in distances if d == distances[0][1]]
        if len(closest) > 1:
            # tie
            continue
        if len(closest) == 1:
            coordinates[closest[0]] += 1
            if infinite:
                infinite_grids.add(closest[0])
    return max([(k, v) for k, v in coordinates.items() if k not in infinite_grids], key=lambda k: k[1]), region_near


def grid_walker(max_x, max_y):
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            yield (y, x)


if __name__ == '__main__':
    _input = map(
        lambda t: t.split(','), open(sys.argv[1]).read().splitlines()
    )
    _input = [(int(y), int(x)) for y, x in _input]
    _input = {(y, x): 0 for y, x in _input}
    # max y and x delimits infinity
    max_y = max([y for y, x in _input])
    max_x = max([x for y, x in _input])


    print('Part 1: {}\nPart 2: {}\n'.format(*solve(_input, int(sys.argv[2]), grid_walker(max_x, max_y))))
