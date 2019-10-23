import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("infile", type=str)


def prep_data(blob):
    patt = re.compile(r"^Disc #\d{1} has (\d+) positions; at time=0, it is at position (\d+)\.$")
    disks = []
    for line in blob.splitlines():
        disks.append(tuple([int(x) for x in patt.search(line).groups()]))
    return disks


def solve(disks):
    time_at_slots = range(1, len(disks) + 1)
    while not all([(start + t) % n == 0 for (n, start), t in zip(disks, time_at_slots)]):
        time_at_slots = [x + 1 for x in time_at_slots]
    return time_at_slots[0] - 1


if __name__ == '__main__':
    args = parser.parse_args()
    disks = prep_data(open(args.infile).read())
    print("Part 1: {:d}".format(solve(disks)))
    disks.append((11, 0))
    print("Part 2: {:d}".format(solve(disks)))
