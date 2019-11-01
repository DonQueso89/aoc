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


def fast_forward(var_to_minimize, new_register,  old_register):
    diff = old_register[var_to_minimize] - new_register[var_to_minimize]
    num_loops_until_zero = new_register[var_to_minimize] / diff
    new_register = {k: v + (new_register[k] - old_register[k]) * num_loops_until_zero for k, v in new_register.items()}
    new_register[var_to_minimize] = 0
    return new_register


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


def solve2(register, instructions):
    pointer = 0
    loop_state = {}
    while True:
        try:
            instr, x, y = instructions[pointer]
        except IndexError:
            return register

        # going into a loop, store the pointer and state
        if loop_state.get(pointer) is None and instr == 'jnz' and y < 0 and register.get(x, 0) != 0:
            loop_state[pointer] = {k: v for k, v in register.items()}
        # hitting the loop a second time, compute fastforward from stored state
        elif loop_state.get(pointer) is not None and instr == 'jnz' and y < 0 and register.get(x, 0) != 0:
            register = fast_forward(x, register, *loop_state[pointer])
            del loop_state[pointer]
        # if the x-value is a constant, we need to jump it so we cant fast forward

        register, pointer, _ = next_state(
            register,
            pointer,
            instr,
            x,
            y,
            0
        )


if __name__ == '__main__':
    args = parser.parse_args()
    inp = open(args.infile).read()
    register, instructions = prep_data(inp)
    print("Part 1: ", solve(register, instructions)[0])
    register, instructions = prep_data(inp)
    register['a'] = 1
    print("Part 2: ", solve2(register, instructions)[1])
