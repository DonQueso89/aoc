#!/usr/bin/env python

import argparse
from day5 import prep_data, intcode_runtime
from ascii_graph import Pyasciigraph
from collections import defaultdict


parser = argparse.ArgumentParser()
parser.add_argument('infile', type=str)


class Node:
    def __init__(self, program, _id):
        self.program = defaultdict(int, {k: v for k, v in program.items()})
        self.inqueue = []
        self.pointer = 0
        self.relative_base = 0
        self._id = _id

        self.outqueue = []
        self.inqueue = [_id, -1]

    def run(self, inputs=None):
        try:
            output, self.pointer, self.program, self.relative_base = intcode_runtime(
                data=self.program,
                _inputs=self.inqueue or [-1],
                pointer=self.pointer,
                feedback_mode=True,
                relative_base=self.relative_base,
            )
            self.outqueue.append(output)
            self.inqueue = []
        except IndexError:
            return None
        return output

    def packet(self):
        if len(self.outqueue) < 3:
            return None

        self.outqueue, _packet = self.outqueue[3:], self.outqueue[:3]
        return _packet

    def __repr__(self):
        return ', '.join([str(x) for x in self.outqueue])


def solve(program):
    nodes = {x: Node(program, x) for x in range(50)}
    idx = 0
    nat = None
    p1 = None
    nat_zero_comm = None
    while True:
        output = -1
        node = nodes[idx]
        while output is not None:
            output = node.run()

            idle = sum([len(x.inqueue) for x in nodes.values()]) == 0
            if idle:
                nodes[0].inqueue += nat
                nat_zero_comm = nat[-1]
                if nat[-1] == nat_zero_comm[-1]:
                    return p1, nat[-1]

            if output == 255:  # intercept NAT packet
                x = node.run()
                y = node.run()
                node.packet()  # remove packet from tx
                nat = [x, y]
                p1 = p1 or y
                break

            packet = node.packet()
            if packet:
                r, x, y = packet
                nodes[r].inqueue += [x, y]

        idx += 1
        idx %= 50

        """
        data = [("node " + str(node._id), len(node.inqueue)) for node in nodes.values()]
        graph = Pyasciigraph()
        for line in graph.graph('rx', data):
            print(line)
        """

    return p1


if __name__ == '__main__':
    args = parser.parse_args()
    data = prep_data(open(args.infile).read())
    print("Part 1: {:d}".format(solve(data)))
