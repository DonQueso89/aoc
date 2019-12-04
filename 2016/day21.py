import argparse
import re


parser = argparse.ArgumentParser()
parser.add_argument("infile", type=str)


def prep_data(blob):
    nodes = []
    for line in blob.splitlines()[2:]:
        x, y, size, used, avail, use = re.findall(r'\d+', line)
        nodes.append((int(x), int(y), int(size), int(used), int(avail)))
    return nodes


def solve(nodes):
    nodes = set(nodes)
    viable = 0
    for node in nodes:
        if node[3] > 0:
            for other in nodes - set([node]):
                if node[3] <= other[4]:
                    viable += 1
    return viable


def solve2(nodes):
    """
    Prefer open paths (without having to move other data)
    Find the nearest node that can host my data.
    If A can not host my data now, find the nearest node that can host A's data
    and so on
    """
    return 0


if __name__ == '__main__':
    args = parser.parse_args()
    nodes = prep_data(open(args.infile).read())
    print('Part 1: {:d}'.format(solve(nodes)))
    print('Part 2: {:d}'.format(solve2(nodes)))
