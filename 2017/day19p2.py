import argparse
import string

parser = argparse.ArgumentParser()
parser.add_argument("infile", type=str)
parser.add_argument("--stopping_char", type=str, default='S', required=False)


STOPCHAR = None

def prep_data(data):
    g = {}
    start_pos = None
    for y, line in enumerate(data.splitlines()):
        for x, c in enumerate(line):
            if start_pos is None and c == '|':
                start_pos = (x, y)
            g[(x, y)] = c
    return g, start_pos


def get_direction(g, x, y, cur_dir):
    if cur_dir in 'NS' and g.get((x - 1, y), '~') in '-' + string.ascii_uppercase:
        return 'W'
    if cur_dir in 'NS' and g.get((x + 1, y), '~') in '-' + string.ascii_uppercase:
        return 'E'
    if cur_dir in 'EW' and g.get((x, y + 1), '~') in '|' + string.ascii_uppercase:
        return 'S'
    if cur_dir in 'EW' and g.get((x, y - 1), '~') in '|' + string.ascii_uppercase:
        return 'N'


def next_pos(x, y, d):
    return {
        'S': lambda x, y: (x, y + 1),
        'N': lambda x, y: (x, y - 1),
        'W': lambda x, y: (x - 1, y),
        'E': lambda x, y: (x + 1, y),
    }[d](x, y)


def print_grid(g, x, y):
    for sy in set([z[1] for z in g]):
        line = ''
        for sx in set([z[0] for z in g]):
            if (sx, sy) == (x, y):
                line += '@'
            else:
                line += g.get((sx, sy), '$')
        print(line)


def solve(g, x, y):
    cur_dir = 'S'
    cur_road = g[(x, y)]
    steps = 1
    while True:
        if cur_road == '+':
            cur_dir = get_direction(g, x, y, cur_dir)
        x, y = next_pos(x, y, cur_dir)
        cur_road = g.get((x, y))
        steps += 1
        if cur_road == STOPCHAR:
            break

    print_grid(g, x, y)
    print(x, y)
    return steps


if __name__ == '__main__':
    args = parser.parse_args()
    inp = open(args.infile).read()
    grid, (sx, sy) = prep_data(inp)
    STOPCHAR = args.stopping_char
    print("Part 2: ", solve(grid, sx, sy))
