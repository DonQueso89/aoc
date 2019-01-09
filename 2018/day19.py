import sys
from day16 import operators


if __name__ == '__main__':
    data = open(sys.argv[1])
    instructions = []
    ip = 0
    registers = [int(sys.argv[2]), 0, 0, 0, 0, 0]
    bound = int(next(data)[-2])

    for instruction in data:
        func, a, b, c = instruction.split()
        a = int(a)
        b = int(b)
        c = int(c)
        instructions.append((func, a, b, c))

    while True:
        registers[bound] = ip
        func, a, b, c = instructions[ip]
        registers[c] = operators[func](a, b, registers)
        ip = registers[bound]
        ip += 1

        if ip < 0 or ip >= len(instructions):
            break
        c += 1
    print("Part 1: " + str(registers[0]))
