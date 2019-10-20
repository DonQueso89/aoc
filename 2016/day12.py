import argparse

parser = argparse.ArgumentParser()
parser.add_argument("infile", type=str)


def prep_data(data):
    instructions = []
    for x in data.splitlines():
        instruction = x.split()
        instructions.append(
            {
                'cpy': lambda i: (i[0], int(i[1]) if i[1][-1].isdigit() else i[1], int(i[2]) if i[2][-1].isdigit() else i[2]),
                'jnz': lambda i: (i[0], int(i[1]) if i[1][-1].isdigit() else i[1], int(i[2]) if i[2][-1].isdigit() else i[2]),
                'inc': lambda i: (i[0], int(i[1]) if i[1].isdigit() else i[1]),
                'dec': lambda i: (i[0], int(i[1]) if i[1].isdigit() else i[1]),
            }[instruction[0]](instruction)
        )
    return {'a': 0, 'b': 0, 'c': 0, 'd': 0}, instructions


def solve(register, instructions):
    pointer = 0
    print(instructions)
    while True:
        try:
            i, x, y = instructions[pointer]
        except IndexError:
            return register
        except ValueError:
            i, x = instructions[pointer]

        pointer_offset = 1
        if i == 'cpy':
            register[y] = register.get(x, x)
        elif i == 'inc':
            register[x] += 1
        elif i == 'dec':
            register[x] -= 1
        elif i == 'jnz' and x != 0:
            pointer_offset = y
        else:
            raise ValueError('Unknown instruction')
        pointer += pointer_offset


if __name__ == '__main__':
    args = parser.parse_args()
    register, instructions = prep_data(open(args.infile).read())
    print("Part 1: ", solve(register, instructions)['a'])
