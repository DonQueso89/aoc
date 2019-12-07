import argparse
import re


parser = argparse.ArgumentParser()
parser.add_argument("infile", type=str)
parser.add_argument("password", type=str)


def prep_data(blob):
    return blob.splitlines()


def solve(scrambles, password):
    """
swap position 5 with position 6
reverse positions 1 through 6
rotate right 7 steps
rotate based on position of letter c
rotate right 7 steps
reverse positions 0 through 4
swap letter f with letter h
reverse positions 1 through 2
move position 1 to position 0
rotate based on position of letter f
move position 6 to position 3
reverse positions 3 through 6
rotate based on position of letter c
rotate based on position of letter b
move position 2 to position 4
swap letter b with letter d
move position 1 to position 6
move position 7 to position 1
swap letter f with letter c
move position 2 to position 3
swap position 1 with position 7
reverse positions 3 through 5
swap position 1 with position 4
move position 4 to position 7
rotate right 4 steps
reverse positions 3 through 6
move position 0 to position 6
swap position 3 with position 5
swap letter e with letter h
rotate based on position of letter c
    """
    _len = len(password)
    for scramble in scrambles:
        if 'rotate right' in scramble:
            op = int(scramble.split()[-2])
            password = password[-op:] + password[:-op]
        elif 'rotate left' in scramble:
            op = int(scramble.split()[-2])
            password = password[op:] + password[:op]
        elif 'rotate based' in scramble:
            op = scramble.split()[-1]
            op = password.index(op) + 1
            if op >= 4:
                op += 1
            op %= _len(password)

        elif 'reverse positions' in scramble:
            s = scramble.split()
            s, e = int(s[-3]), int(s[-1])
        elif 'swap position' in scramble:
            s = scramble.split()
            s, e = int(s[-4]), int(s[-1])
        elif 'swap letter' in scramble:
            s = scramble.split()
            s, e = password.index(s[-4]), password.index(s[-1])
        elif 'move position' in scramble:
            s = scramble.split()
            s, e = int(s[-4]), int(s[-1])
            x = password[2]
            password = password[:s] + password[s:e] + x + password[e:]


        else:
            raise Exception('hit unknown operation')


if __name__ == '__main__':
    args = parser.parse_args()
    data = prep_data(open(args.infile).read())
    print('Part 1: {}'.format(solve(data)))
