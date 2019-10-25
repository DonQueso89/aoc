import argparse

parser = argparse.ArgumentParser()
parser.add_argument("infile", type=str)
parser.add_argument("max_depth", type=int)


def intcoded(row):
    """
    Given row of lenght n like 01010
    return list<int> of length n where each element i is the base-10 representation
    of the [i - 1: i + 2] slice of the input
    if the slice is out of bounds the coded version is padded with 0.
    e.g.:
        input  001101
        output 013652
    """
    int_coded = []

    for i in range(len(row)):
        if i == len(row):
            int_coded.append(int(row[i-1:], 2))
        elif i == 0:
            int_coded.append(int(row[:i+2], 2))
        else:
            int_coded.append(int(row[i-1:i+2], 2))
    return int_coded


safe = set([2, 5, 7, 0])


def solve(row, num_rows):
    # next row is function of previous row
    # safe tiles are 2, 5, 7 (010, 101, 111)
    # for the last elem, 1 is safe and 2 is a trap
    count = 0
    loops = 0
    while loops < num_rows:
        count += row.count('0')
        row = intcoded(row)
        next_row = ""
        for e in row[:-1]:
            if e in safe:
                next_row += '0'
            else:
                next_row += '1'
        next_row += '0' if row[-1] in {1, 0} else '1'
        row = next_row
        loops += 1
    return count


if __name__ == '__main__':
    args = parser.parse_args()
    row = open(args.infile).read()
    print('Part 1: {:d}'.format(solve(row.replace('^', '1').replace('.', '0'), args.max_depth)))
