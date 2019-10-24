import argparse
import hashlib
import re

parser = argparse.ArgumentParser()
parser.add_argument("passcode", type=str)
parser.add_argument("width", type=int)
parser.add_argument("height", type=int)


def prep_data(w, h):
    grid = set()
    for y in range(h):
        for x in range(w):
            grid.add((x, y))
    return grid


room_directions = [
    (0, -1, 'U'),
    (0, 1, 'D'),
    (-1, 0, 'L'),
    (1, 0, 'R')
]


def solve(path, x=0, y=0, target_x=3, target_y=3):
    if solve.result:
        if len(path) >= len(solve.result[0]):
            return
        if (x, y) == (target_x, target_y):
            solve.result.pop()
            solve.result.append(path)
            return

    if (x, y) == (target_x, target_y):
        solve.result.append(path)
        return

    room_hash = hashlib.md5(path.encode()).hexdigest()[:4]
    for i, (dx, dy, d) in enumerate(room_directions):
        if (x + dx, y + dy) in solve.maze and room_hash[i] in 'bcdef':
            solve(
                path + d,
                x + dx,
                y + dy,
                target_x,
                target_y,
            )


def solve2(path, x=0, y=0, target_x=3, target_y=3):
    if solve2.result:
        if (x, y) == (target_x, target_y):
            if len(path) > len(solve2.result[0]):
                solve2.result.pop()
                solve2.result.append(path)
            return
    elif (x, y) == (target_x, target_y):
        solve2.result.append(path)
        return

    room_hash = hashlib.md5(path.encode()).hexdigest()[:4]
    for i, (dx, dy, d) in enumerate(room_directions):
        if (x + dx, y + dy) in solve2.maze and room_hash[i] in 'bcdef':
            solve2(
                path + d,
                x + dx,
                y + dy,
                target_x,
                target_y,
            )


if __name__ == '__main__':
    args = parser.parse_args()
    result = []
    solve.result = result
    solve.maze = prep_data(args.width, args.height)
    solve(args.passcode)
    shortest = re.search('^[a-z]+([UDLR]+)$', result[0]).groups()[0]
    print("Part 1: {}".format(shortest))

    result = []
    solve2.result = result
    solve2.maze = prep_data(args.width, args.height)
    solve2(args.passcode)
    longest = len(re.search('^[a-z]+([UDLR]+)$', result[0]).groups()[0])
    print("Part 2: {}".format(longest))
