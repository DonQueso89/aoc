import argparse
import re
from collections import defaultdict
from functools import partial

parser = argparse.ArgumentParser()
parser.add_argument("infile", type=str)


def meta_transform(state, p1, p2):
    return p1 + p2, state


def prep_data(data):
    _iter = (x for x in data.splitlines())
    state = re.search(r'.*state ([A-F]{1}).*', next(_iter)).groups()[0]
    num_steps = int(re.search(r'.* (\d+) steps.*', next(_iter)).groups()[0])
    next(_iter)

    transformations = {}
    meta_transformations = {}
    while True:
        in_state = next(_iter)[-2]
        next(_iter)
        zero_out = int(next(_iter)[-2])
        zero_pointer_incr = 1 if 'right' in next(_iter) else -1
        zero_next_state = next(_iter)[-2]
        next(_iter)
        one_out = int(next(_iter)[-2])
        one_pointer_incr = 1 if 'right' in next(_iter) else -1
        one_next_state = next(_iter)[-2]

        transformations[in_state] = {
            (1, 0): lambda b: b ^ 1,
            (1, 1): lambda b: b | 1,
            (0, 0): lambda b: b & 0,
            (0, 1): lambda b: b | 0,
        }[(zero_out, one_out)]

        meta_transformations[in_state] = {
            0: partial(meta_transform, zero_next_state, zero_pointer_incr),
            1: partial(meta_transform, one_next_state, one_pointer_incr),
        }
        try:
            next(_iter)
        except StopIteration:
            break

    return state, num_steps, transformations, meta_transformations


def solve(state, num_steps, transformations, meta_transformations):
    tape = defaultdict(lambda: 0)
    pointer = 0
    while num_steps:
        val = tape[pointer]
        tape[pointer] = transformations[state](val)
        pointer, state = meta_transformations[state][val](pointer)
        num_steps -= 1
    return sum(tape.values())


if __name__ == '__main__':
    args = parser.parse_args()
    inp = open(args.infile).read()
    print("Part 1: ", solve(*prep_data(inp)))
