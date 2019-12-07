#!/usr/bin/env python

import argparse
from day5 import intcode_runtime
from itertools import permutations


parser = argparse.ArgumentParser()
parser.add_argument('infile', type=str)
parser.add_argument('input', type=int)


def prep_data(blob):
    return [int(x) for x in blob.split(',')]


def collect_outputs(program, _input, phase_range, outputs, depth=5):
    for phase_setting in phase_range:
        _program = [x for x in program]
        output = intcode_runtime(_program, [phase_setting, _input], 0, False)
        if depth == 1:
            outputs.append(output)
        else:
            collect_outputs(
                _program,
                output,
                phase_range - set([phase_setting]),
                outputs,
                depth - 1,
            )


def solve(program, _input):
    outputs = []
    collect_outputs(program, _input, {0, 1, 2, 3, 4}, outputs)
    return max(outputs)


def feedback(program, _input, phase_cfg):
    print("TESTING PERM ", phase_cfg)
    amp_states = {
        x: (0, 0, [x for x in program], [phase_cfg.pop()]) for x in range(1, 5)
    }  # amp-no.: (last_output, pointer, program, inputs)
    print("TESTING PERM ", amp_states)

    # bootstrap A with input signal
    output, pointer, program = intcode_runtime(
        [x for x in program],
        [phase_cfg.pop(), _input],
        0,
        True
    )
    amp_states[0] = (output, pointer, program, [])

    amp_states[1][3].append(output)
    amp = 1
    while True:
        output, pointer, program = intcode_runtime(
            amp_states[amp][2],
            amp_states[amp][3] + [output],
            amp_states[amp][1],
            True,
        )
        amp_states[amp] = (output, pointer, program, [])
        if program is None:
            return amp_states[4][0]
        amp = (amp + 1) % 5


def solve2(program, _input):
    thruster_signal = 0
    for c in permutations([5, 6, 7, 8, 9], 5):
        thruster_signal = max(feedback(program, _input, list(c)), thruster_signal)
    return thruster_signal


if __name__ == '__main__':
    args = parser.parse_args()
    program = prep_data(open(args.infile).read())
    #print("Part 1: {:d}".format(solve(program, args.input)))
    print("Part 2: {:d}".format(solve2(program, args.input)))
