import sys
from functools import partial


def potstate(transformations, state, zero_offset):
    # Range of interest is [left most plant idx - 2; rightmost plant idx + 2]
    # Add empty pots to the state if this is necessary
    leftmost_plant = state.index("#")
    rightmost_plant = len(state) - state[::-1].index("#") - 1
    if leftmost_plant - 2 < 0:
        left_incr = abs(leftmost_plant - 2)
        state = ("." * left_incr) + state
        zero_offset += left_incr
    if rightmost_plant + 2 >= len(state):
        right_incr = (rightmost_plant + 3) - len(state)
        state += "." * right_incr

    new_state = ""
    for idx, pot in enumerate(state):
        invisible_pots = max(0, (idx + 3) - len(state))
        lookaround = state[max(0, idx - 2):  idx + 3] + "." * invisible_pots
        new_state += transformations.get(
            int(lookaround.replace('#', '1').replace('.', '0'), 2),
            '.'
        )
    return new_state, zero_offset


if __name__ == '__main__':
    data = open(sys.argv[1])
    num_generations = int(sys.argv[2])
    part_to_solve = int(sys.argv[3])
    state = next(data).split()[2]
    data = [x.strip() for x in data]
    transformations = [
        (x.split("=>")[0].strip(), x.split("=>")[1].strip()) for x in data if "=>" in x
    ]
    # make the keys binary strings and parse them into ints so we can lose the
    # padding dots when we doing the lookups
    transformations = {
        int(k.replace("#", "1").replace(".", "0"), 2): v for k, v in transformations
    }
    zero_offset = 0
    potsgenerator = partial(potstate, transformations)

    if part_to_solve == 1:
        for i in range(num_generations):
            state, zero_offset = potsgenerator(state, zero_offset)

        result = 0
        for idx, potnumber in enumerate(range(zero_offset * -1, len(state) - zero_offset)):
            if state[idx] == "#":
                result += potnumber

        print("Part 1: " + str(result))
    else:
        # After some time the result increases linearly
        search_depth = 1100
        for i in range(search_depth):
            state, zero_offset = potsgenerator(state, zero_offset)
            if i == 999:
                thousandth_generation = sum([potnumber for idx, potnumber in enumerate(range(zero_offset * -1, len(state) - zero_offset)) if state[idx] == '#'])
        result = sum([potnumber for idx, potnumber in enumerate(range(zero_offset * -1, len(state) - zero_offset)) if state[idx] == '#'])

        result += (result - thousandth_generation) * ((num_generations - search_depth) // 100)
        print("Part 2: " + str(result))
