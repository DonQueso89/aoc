import time
import argparse
from collections import defaultdict
from functools import partial

parser = argparse.ArgumentParser(description='Solve day 22')
parser.add_argument('depth', type=int, help='depth of cave')
parser.add_argument('targetX', type=int, help='target x coordinate')
parser.add_argument('targetY', type=int, help='target y coordinate')


'''
start with the torch equipped at (0, 0)
In rocky regions, you can use the climbing gear or the torch. You cannot use neither (you'll likely slip and fall).
In wet regions, you can use the climbing gear or neither tool. You cannot use the torch (if it gets wet, you won't have a light source).
In narrow regions, you can use the torch or neither tool. You cannot use the climbing gear (it's too bulky to fit).
At the end, you need the torch
'''


ROCK = 0
WET = 1
NARROW = 2

NEITHER = 0
TORCH = 1
CLIMBING_GEAR = 2

valid_for_rock = set([CLIMBING_GEAR, TORCH])
valid_for_wet = set([CLIMBING_GEAR, NEITHER])
valid_for_narrow = set([TORCH, NEITHER])

valid_for = {
    ROCK: valid_for_rock,
    WET: valid_for_wet,
    NARROW: valid_for_narrow
}


def neighbours(max_x, max_y, tx, ty, x, y):
    for offsetX, offsetY in [
        (0, 1),
        (1, 0),
        (-1, 0),
        (0, -1)
    ]:
        sx, sy = x + offsetX, y + offsetY
        if (sx, sy) == (tx, ty):
            yield (sx, sy)
            break
        if sx >= 0 and sx <= max_x and sy >= 0 and sy <= max_y:
            yield (sx, sy)


def possible_paths_with_costs(cave_map, neighbour_generator, x, y, current_tool):
    """
    For each path, return 3tuple of ((x, y), required tool, associated cost)
    """
    current_region = cave_map[(x, y)]
    neighbours = {(nx, ny): cave_map[(nx, ny)] for nx, ny in neighbour_generator(x, y)}
    can_switch_to = valid_for[current_region]
    current_tool = set([current_tool])
    neighbours_with_costs = []

    for coordinate, neighbour_type in neighbours.items():
        valid_for_neighbour = valid_for[neighbour_type]
        # We can move to it without switching
        if current_tool & valid_for_neighbour:
            neighbours_with_costs.append((coordinate, list(current_tool)[0], 1))
            continue
        # We can move to it by switching
        switch_to = can_switch_to & valid_for_neighbour
        if switch_to:
            neighbours_with_costs.append((coordinate, list(switch_to)[0], 8))

    return neighbours_with_costs


def get_erosion_level(erosion_levels, depth, x, y):
    if y == 0:
        return (x * 16807 + depth) % 20183
    if x == 0:
        return (y * 48271 + depth) % 20183
    return (erosion_levels[(x - 1, y)] * erosion_levels[(x, y - 1)] + depth) % 20183


def distance_from_target(target, coord):
    tx, ty = target
    cx, cy = coord
    return abs(tx - cx) + abs(ty - cy)


def display(cave_map, tx, ty, cx, cy):
    result = ""
    for y in range(0, max(cave_map.keys(), key=lambda k: k[1])[1] + 1):
        result += '\n'
        for x in range(0, max(cave_map.keys(), key=lambda k: k[0])[0] + 1):
            if (cx, cy) == (x, y):
                result += " X"
            elif (tx, ty) == (x, y):
                result += " T"
            else:
                result += (" " + str(cave_map[(x, y)]))
    print(result)



if __name__ == '__main__':
    args = parser.parse_args()
    depth, tx, ty = args.depth, args.targetX, args.targetY
    erosion_levels = defaultdict(int)
    erosion_levels[(0, 0)] = 0

    get_erosion_level = partial(get_erosion_level, erosion_levels, depth)

    # Calculate west and north borders first to avoid the overhead of checking
    # whether the coordinate is the cavemouth on every iteration
    # North border
    for y in range(0, 1):
        for x in range(1, tx + 1):
            erosion_levels[(x, y)] = get_erosion_level(x, y)

    # West border
    for y in range(1, ty + 1):
        for x in range(0, 1):
            erosion_levels[(x, y)] = get_erosion_level(x, y)

    for y in range(1, ty + 1):
        for x in range(1, tx + 1):
            erosion_levels[(x, y)] = get_erosion_level(x, y)

    erosion_levels[(tx, ty)] = 0
    cave_map = {coordinate: el % 3 for coordinate, el in erosion_levels.items()}
    risk_level = sum(list(cave_map.values()))
    print("Part 1: " + str(risk_level))

    neighbours_func = partial(neighbours, tx, ty, tx, ty)
    get_paths_with_costs = partial(
        possible_paths_with_costs,
        cave_map,
        neighbours_func
    )
    removed_from_target = partial(distance_from_target, (tx, ty))

    last = (0, 0)
    x, y = last
    current_tool = TORCH
    total_cost = 0
    max_x, max_y = tx, ty
    display = partial(display, cave_map, tx, ty)
    while (x, y) != (tx, ty):
        # Dont consider where we came from
        display(x, y)
        print(total_cost)
        paths = [p for p in get_paths_with_costs(x, y, current_tool) if p[0] != last]

        low_cost = [p for p in paths if p[2] == 1]
        high_cost = [p for p in paths if p[2] == 8]
        candidates = low_cost or high_cost
        last = (x, y)
        # Only 1 optimal candidate
        if len(candidates) == 1:
            next_region = candidates[0]
            x, y = next_region[0]
            current_tool = next_region[1]
            total_cost += next_region[2]
        # Multiple optimal candidates, choose the one closest to the target
        elif len(candidates) > 1:
            next_region = sorted(candidates, key=lambda k: removed_from_target(k[0]))[0]
            x, y = next_region[0]
            current_tool = next_region[1]
            total_cost += next_region[2]

        # Increase reach when necessary
        if x == max_x or y == max_y:
            max_x += 1
            max_y += 1

            # East border
            for sy in range(0, max_y + 1):
                for sx in range(max_x, max_x + 1):
                    cave_map[(sx, sy)] = get_erosion_level(sx, sy) % 3

            # South border
            for sy in range(max_y, max_y + 1):
                for sx in range(0, max_x + 1):
                    cave_map[(sx, sy)] = get_erosion_level(sx, sy) % 3

            # Update neighbours func
            neighbours_func = partial(neighbours, max_x, max_y, tx, ty)
        time.sleep(2)
    if current_tool != TORCH:
        total_cost += 7
    print("Part 2: " + str(total_cost))
