import re
import argparse
from collections import defaultdict

parser = argparse.ArgumentParser(description='Solve day 23')
parser.add_argument("infile", type=str)


def solve(path):
    rooms_discovered = defaultdict(list)
    stack = []  # []<(num_doors, (x, y))>
    char = path[0]
    idx = 1
    dirs = set('SNEW')
    num_doors = 0
    cur_pos = (0, 0)
    branchpoint = (None, 0)
    while char != '$':
        char = path[idx]
        if char in dirs:
            cur_pos = {
                'W': lambda x: (x[0] - 1, x[1]),
                'E': lambda x: (x[0] + 1, x[1]),
                'S': lambda x: (x[0], x[1] - 1),
                'N': lambda x: (x[0], x[1] + 1),
            }[char](cur_pos)
            num_doors += 1
            rooms_discovered[cur_pos].append(num_doors)
        elif char == '|':
            num_doors, cur_pos = branchpoint
            if path[idx + 1] == ')':
                branchpoint = stack.pop()
                idx += 2
                continue
        elif char == '(':
            stack.append(branchpoint)
            branchpoint = (num_doors, cur_pos)
        elif char == ')':
            branchpoint = stack.pop()
        idx += 1

    shortest_paths = [min(v) for v in rooms_discovered.values()]
    return max(shortest_paths), len([x for x in shortest_paths if x >= 1000])


if __name__ == '__main__':
    args = parser.parse_args()
    data = open(args.infile).read()
    d1, d2 = solve(data)
    print("Part 1: {:d}".format(d1))
    print("Part 2: {:d}".format(d2))
