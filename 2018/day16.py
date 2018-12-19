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


if __name__ == '__main__':
    data = open('input16p1').read().splitlines()
    cnt = 0
    opcodes = defaultdict(list)
    for i in range(0, len(data), 4):
        before = [int(x) for x in re.sub(rgx, ' ', data[i]).strip().split()]
        opcode, a, b, c = [int(x) for x in re.sub(rgx, ' ', data[i + 1]).strip().split()]
        after = [int(x) for x in re.sub(rgx, ' ', data[i + 2]).strip().split()]
        func_cnt = 0
        for opname, operator in operators.items():
            tmp = before.copy()
            tmp[c] = operator(a, b, before)
            if tmp == after:
                opcodes[opcode].append(opname)
                func_cnt += 1
        if func_cnt >= 3:
            cnt += 1
    print("Part 1: " + str(cnt))
    print(opcodes)
    opcode2opname = {opcode: Counter(opnames).most_common()[0][0] for opcode, opnames in opcodes.items()}

    program = open('input16p2').read().splitlines()
    registers = [0, 0, 0, 0]
    for instruction in program:
        print("State " + str(registers))
        opcode, a, b, c = [int(x) for x in instruction.strip().split()]
        print("Executing {} a: {} b: {} c: {}".format(opcode2opname[opcode], a, b, c))
        registers[c] = operators[opcode2opname[opcode]](a, b, registers)

    print("Part 2: " + str(registers[0]))
