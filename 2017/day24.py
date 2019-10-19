import argparse

parser = argparse.ArgumentParser()
parser.add_argument("infile", type=str)


def prep_data(data):
    return set([tuple([int(y) for y in x.split('/')]) for x in data.splitlines()])


def solve(remaining_components, last_port, current_sum, depth, result):
    can_connect = set([x for x in remaining_components if last_port in x])
    if not can_connect:
        result.append((current_sum, depth))
        return
    for c in can_connect:
        next_port = list((set(c) - set([last_port])))
        solve(
            remaining_components - set([c]),
            next_port[0] if next_port else last_port,
            current_sum + sum(c),
            depth + 1,
            result
        )


if __name__ == '__main__':
    args = parser.parse_args()
    inp = open(args.infile).read()
    components = prep_data(inp)
    result = []
    solve(components, 0, 0, 0, result)
    print("Part 1: ", max([x[0] for x in result]))
    print("Part 2: ", sorted(result, key=lambda k: (k[1], k[0]))[-1])
