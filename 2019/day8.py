#!/usr/bin/env python

import argparse
import numpy as np


parser = argparse.ArgumentParser()
parser.add_argument('infile', type=str)


def prep_data(blob, width, height):
    blob = list(blob)
    layers = []
    while blob:
        layer = []
        for x in range(width * height):
            layer.append(int(blob.pop(0)))
        layers.append(layer)
    return layers


def solve(layers, width, height):
    min_layer, min_zeros = None, 1 << 64
    picture = np.zeros((height, width))
    picture.fill(2)
    for layer in layers:
        cnt = 0
        for i, pixel in enumerate(layer):
            x, y = i // width, i % width
            if pixel == 0:
                cnt += 1
                if picture[x][y] == 2:
                    picture[x][y] = 0
            elif pixel == 1 and picture[x][y] == 2:
                picture[x][y] = 1
        if cnt < min_zeros:
            min_layer, min_zeros = layer, cnt

    picture = np.vectorize(lambda k: '$' if k == 0 else ' ')(picture)
    print("Part 2:")
    print("$" * width)
    for row in picture:
        print("".join(row))
    print("$" * width)
    return min_layer.count(1) * min_layer.count(2)


if __name__ == '__main__':
    args = parser.parse_args()
    data = prep_data(open(args.infile).read(), 25, 6)
    print("Part 1: {:d}".format(solve(data, 25, 6)))
