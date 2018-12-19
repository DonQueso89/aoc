import re
from collections import defaultdict, Counter
'''
Addition:

addr (add register) stores into register C the result of adding register A and register B.
addi (add immediate) stores into register C the result of adding register A and value B.
Multiplication:

mulr (multiply register) stores into register C the result of multiplying register A and register B.
muli (multiply immediate) stores into register C the result of multiplying register A and value B.
Bitwise AND:

banr (bitwise AND register) stores into register C the result of the bitwise AND of register A and register B.
bani (bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B.
Bitwise OR:

borr (bitwise OR register) stores into register C the result of the bitwise OR of register A and register B.
bori (bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B.
Assignment:

setr (set register) copies the contents of register A into register C. (Input B is ignored.)
seti (set immediate) stores value A into register C. (Input B is ignored.)
Greater-than testing:

gtir (greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0.
gtri (greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0.
gtrr (greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0.
Equality testing:

eqir (equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0.
eqri (equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0.
eqrr (equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0.
'''
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
    opcodes = defaultdict(set)
    for i in range(0, len(data), 4):
        before = [int(x) for x in re.sub(rgx, ' ', data[i]).strip().split()]
        opcode, a, b, c = [int(x) for x in re.sub(rgx, ' ', data[i + 1]).strip().split()]
        after = [int(x) for x in re.sub(rgx, ' ', data[i + 2]).strip().split()]
        func_cnt = 0
        for opname, operator in operators.items():
            tmp = before.copy()
            tmp[c] = operator(a, b, before)
            if tmp == after:
                opcodes[opcode] |= (opcodes[opcode] & {opname})
                func_cnt += 1
        if func_cnt >= 3:
            cnt += 1
    print("Part 1: " + str(cnt))
    print(opcodes)
    opcode2opname = {opcode: list(opnames)[0] for opcode, opnames in opcodes.items()}

    program = open('input16p2').read().splitlines()
    registers = [0, 0, 0, 0]

    for instruction in program:
        opcode, a, b, c = [int(x) for x in instruction.strip().split()]
        registers[c] = operators[opcode2opname[opcode]](a, b, registers)

    print("Part 2: " + str(registers[0]))
