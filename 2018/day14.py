import sys


def solve(num_recipes):
    """
        This actually  only solves the second part hehe
    """
    elf0, elf1 = 0, 1
    recipes = [3, 7]

    # pt2
    num_done = 2
    match_sequence = [int(x) for x in list(str(num_recipes))]
    last_n = [None] * (len(match_sequence) - 2) + recipes

    num_recipes += 8

    while True:
        r0, r1 = recipes[elf0], recipes[elf1]
        for x in str(r1 + r0):
            y = int(x)
            recipes.append(int(y))
            last_n.append(y)
            last_n.pop(0)
            num_recipes -= 1
            num_done += 1
            if last_n == match_sequence:
                return recipes[-10 + num_recipes:num_recipes],  num_done - len(match_sequence)

        elf0 = (elf0 + r0 + 1) % len(recipes)
        elf1 = (elf1 + r1 + 1) % len(recipes)
    return recipes[-10 + num_recipes:]


if __name__ == '__main__':
    num_recipes = int(sys.argv[1])
    print(solve(num_recipes))
