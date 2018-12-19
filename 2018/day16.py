import re
from collections import defaultdict, Counter

operators = {
    'addr': lambda a, b, r: r[a] + r[b],
    'addi': lambda a, b, r: r[a] + b,
    'mulr': lambda a, b, r: r[a] * r[b],
    'muli': lambda a, b, r: r[a] * b,
    'banr': lambda a, b, r: r[a] & r[b],
    'bani': lambda a, b, r: r[a] & b,
    'borr': lambda a, b, r: r[a] | r[b],
    'bori': lambda a, b, r: r[a] | b,
    'setr': lambda a, b, r: r[a],
    'seti': lambda a, b, r: a,
    'gtir': lambda a, b, r: 1 if a > r[b] else 0,
    'gtri': lambda a, b, r: 1 if r[a] > b else 0,
    'gtrr': lambda a, b, r: 1 if r[a] > r[b] else 0,
    'eqir': lambda a, b, r: 1 if a == r[b] else 0,
    'eqri': lambda a, b, r: 1 if r[a] == b else 0,
    'eqrr': lambda a, b, r: 1 if r[a] == r[b] else 0
}


rgx = re.compile(r'[^\d]')


def num_funcs_applicable(testops, a, b, c, before, after):
    func_cnt = 0
    last_op = None
    for opname, operator in testops.items():
        tmp = before.copy()
        tmp[c] = operator(a, b, before)
        if tmp == after:
            last_op = opname
            func_cnt += 1
    return func_cnt, last_op


if __name__ == '__main__':
    data = open('input16p1').read().splitlines()
    cnt = 0
    samples_per_opcode = defaultdict(list)   # storage for number resolution p2
    for i in range(0, len(data), 4):
        before = [int(x) for x in re.sub(rgx, ' ', data[i]).strip().split()]
        opcode, a, b, c = [int(x) for x in re.sub(rgx, ' ', data[i + 1]).strip().split()]
        after = [int(x) for x in re.sub(rgx, ' ', data[i + 2]).strip().split()]
        func_cnt, _ = num_funcs_applicable(operators, a, b, c, before, after)
        if func_cnt >= 3:
            cnt += 1
        samples_per_opcode[opcode].append((a, b, c, before, after))
    print("Part 1: " + str(cnt))

    # Figure out number-opcode mapping by knockout
    opcode2opname = {}

    knockout = operators.copy()
    while len(opcode2opname) < len(operators):
        for opcode, samples in samples_per_opcode.items():
            func_cnt, opname = num_funcs_applicable(knockout, *samples[0])
            if func_cnt == 1:
                opcode2opname[opcode] = opname
                samples_per_opcode.pop(opcode)
                knockout.pop(opname)
                break

    program = open('input16p2').read().splitlines()
    registers = [0, 0, 0, 0]
    for instruction in program:
        opcode, a, b, c = [int(x) for x in instruction.strip().split()]
        registers[c] = operators[opcode2opname[opcode]](a, b, registers)
    print("Part 2: " + str(registers[0]))
