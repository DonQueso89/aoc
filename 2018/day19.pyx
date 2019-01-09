from day16 import operators


if __name__ == '__main__':
    data = open('input19')
    instructions = []
    ip = 0
    registers = {0: 1, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
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
        print(registers)

        if ip < 0 or ip >= len(instructions):
            break
    print("Part 2: " + str(registers[0]))
