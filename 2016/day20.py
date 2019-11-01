import argparse


parser = argparse.ArgumentParser()
parser.add_argument("infile", type=str)


def prep_data(blob):
    return [tuple([int(x) for x in y.split('-')]) for y in blob.splitlines()]


def contained(start, end, ips):
    for bstart, bend in ips:
        if bstart <= start <= end <= bend:
            return True
    return False


def clipped_range(start, end, ips):
    """
    a [1][2][3][4]
    b          [4][5][6][7]
    becomes
    a [1][2][3]
    b          [4][5][6][7]
    ----------------------
    a [1][2][3][4]
    b    [2][3][4][5][6][7]
    becomes
    a [1]
    b    [2][3][4][5][6][7]
    """
    print(start, end)
    for bstart, bend in ips:
        if bstart < start <= bend < end:
            print("overlap left")
            start = bend + 1
        elif start < bstart <= end < bend:
            print("overlap right")
            end = bstart - 1
    print(start, end)
    return start, end


def solve(blocked_ranges):
    blocked_ranges = sorted(blocked_ranges, key=lambda k: k[0])
    last_end = blocked_ranges[0][1]
    minimal_allowed = None

    for start, end in blocked_ranges[1:]:
        if start > last_end + 1:
            if minimal_allowed is None:
                minimal_allowed = last_end + 1
        last_end = end

    # Remove full overlaps
    blocked_ranges = set(blocked_ranges)
    ranges_checked = set()
    partially_overlapping_ranges = set()
    for start, end in blocked_ranges:
        ranges_checked.add((start, end))
        if contained(start, end, blocked_ranges - ranges_checked):
            continue
        else:
            partially_overlapping_ranges.add((start, end))

    # Clip partial overlaps
    ranges_checked = set()
    non_overlapping_ranges = set()
    for start, end in partially_overlapping_ranges:
        clipped_start, clipped_end = clipped_range(
            start,
            end,
            partially_overlapping_ranges - ranges_checked,
        )
        ranges_checked.add((start, end))
        non_overlapping_ranges.add((clipped_start, clipped_end))

    total_allowed = 1 << 32
    for start, end in non_overlapping_ranges:
        print(total_allowed)
        if start == end:
            total_allowed -= 1
        elif end - start == 1:
            total_allowed -= 2
        elif start > end:
            raise Exception("Start must be <= end")
        else:
            total_allowed -= ((end - start) + 2)

    return minimal_allowed, total_allowed


if __name__ == '__main__':
    args = parser.parse_args()
    blocked_ranges = prep_data(open(args.infile).read())
    minimal_allowed, total_allowed = solve(blocked_ranges)
    print('Part 1: {:d}'.format(minimal_allowed))
    print('Part 2: {:d}'.format(total_allowed))
