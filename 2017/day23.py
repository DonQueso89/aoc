import argparse
import string

parser = argparse.ArgumentParser()
parser.add_argument("infile", type=str)


def prep_data(data):
    register = {}
    instructions = []
    for line in data.splitlines():
        instr, x, y = line.strip().split(" ")
        instructions.append((instr, int(x) if x[-1].isdigit() else x, int(y) if y[-1].isdigit() else y))
        if x in string.ascii_lowercase:
            register[x] = 0
        if y in string.ascii_lowercase:
            register[y] = 0
    return register, instructions


def next_state(register, pointer, instr, x, y, num_mults):
    if instr == 'mul':
        num_mults += 1
        register[x] *= register.get(y, y)
        pointer += 1
    elif instr == 'jnz':
        if register.get(x, x) != 0:
            pointer = (pointer + register.get(y, y))
        else:
            pointer += 1
    elif instr == 'set':
        register[x] = register.get(y, y)
        pointer += 1
    elif instr == 'sub':
        register[x] -= register.get(y, y)
        pointer += 1
    else:
        raise Exception("Invalid instruction")
    return register, pointer, num_mults


def solve(register, instructions):
    pointer = 0
    num_mults = 0
    while True:
        try:
            instr, x, y = instructions[pointer]
        except IndexError:
            return num_mults, register
        register, pointer, num_mults = next_state(
            register,
            pointer,
            instr,
            x,
            y,
            num_mults
        )


def solve2():
    """
    This is just manually investigating and understanding the instructionset
    """
    s = 0
    def isprime(n):
        for i in range(2, n // 2):
            if n % i == 0:
                return False
        return True

    for y in range(105700, 122700 + 1, 17):
        if not isprime(y):
            s += 1
    return s


if __name__ == '__main__':
    args = parser.parse_args()
    inp = open(args.infile).read()
    register, instructions = prep_data(inp)
    print("Part 1: ", solve(register, instructions)[0])
    print("Part 2: {:d}".format(solve2()))
