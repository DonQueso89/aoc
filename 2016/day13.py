import argparse

parser = argparse.ArgumentParser()
parser.add_argument("magic_number", type=int)
parser.add_argument("target_x", type=int)
parser.add_argument("target_y", type=int)
parser.add_argument("extra_space_x", type=int)
parser.add_argument("extra_space_y", type=int)


def prep_data(target_x, target_y, magic_number, extra_space_x, extra_space_y):
    maze = {}
    for y in range(target_y + extra_space_y):
        line = ''
        for x in range(target_x + extra_space_x):
            n = x ** 2 + 3 * x + 2 * x * y + y + y ** 2 + magic_number
            if bin(n).count('1') % 2 == 0:
                maze[(x, y)] = ' '
                line += '.'
            else:
                maze[(x, y)] = '#'
                line += '#'
    return maze


def print_maze(paths, maze, target_x, target_y):
    for y in range(max(maze)[1]):
        line = ''
        for x in range(max(maze)[0]):
            d = paths.get((x, y))
            if (x, y) == (target_x, target_y):
                line += '@'
            elif d is not None:
                line += '$'
            else:
                line += maze[(x, y)]
        print(line)


def solve(maze, target_x, target_y):
    """
    Solve maze by flood-filling it.
    """
    paths = {(1, 1): 0}

    while True:
        possible_steps = {}
        for (x, y), distance in paths.items():
            steps = (s for s in [
                (x + 1, y),
                (x, y + 1),
                (x, y - 1),
                (x - 1, y)] if maze.get(s) == ' ')

            if steps:
                for step in steps:
                    if (target_x, target_y) == step:
                        print_maze(paths, maze, target_x, target_y)
                        return distance + 1, len(set([c for c, d in paths.items() if d <= 50]))
                    if paths.get(step, 9999999) > distance + 1 and possible_steps.get(step, 9999999) > distance + 1:
                        possible_steps[step] = distance + 1

        if possible_steps:
            for k, v in possible_steps.items():
                paths[k] = v
        else:
            print_maze(paths, maze, target_x, target_y)
            raise Exception("Dead end without reaching target")


if __name__ == '__main__':
    args = parser.parse_args()
    maze = prep_data(
        args.target_x,
        args.target_y,
        args.magic_number,
        args.extra_space_x,
        args.extra_space_y,
    )

    print("Part 1: {:d}\nPart 2: {:d}".format(*solve(
        maze,
        args.target_x,
        args.target_y
    )))
