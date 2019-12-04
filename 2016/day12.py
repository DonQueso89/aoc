import argparse


parser = argparse.ArgumentParser()
parser.add_argument("infile", type=str)


def prep_data(blob):
    return [tuple([int(y) if y.lstrip('-').isdigit() else y for y in x.split()]) for x in blob.splitlines()]


def solve(instructions, register):
    eof = len(instructions)
    pointer = 0
    while pointer < eof:
        offset = 1
        instr, args = instructions[pointer][0], instructions[pointer][1:]
        if pointer == 16:
            print(register, instr, args)
        if instr == 'cpy':
            x, y = args
            register[y] = register.get(x, x)
        elif instr == 'jnz':
            x, y = args
            if register.get(x, x) != 0:
                offset = y
        else:
            x = args[0]
            register[x] = register[x] + 1 if instr == 'inc' else register[x] - 1
        pointer += offset
    return register['a']


if __name__ == '__main__':
    args = parser.parse_args()
    instructions = prep_data(open(args.infile).read())
    print('Part 1: {:d}'.format(solve(instructions, {x: 0 for x in 'abcd'})))
    print('Part 2: {:d}'.format(solve(instructions, {'a': 0, 'b': 0, 'c': 1, 'd': 0})))
