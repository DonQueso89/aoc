import re
import random
import time


class Light(object):
    deltas = (-1, 0), (0, 1), (1, 0), (0, -1)

    def __init__(self, x, y, xv, yv):
        self.x = x
        self.y = y
        self.xv = xv
        self.yv = yv

    def tick(self):
        self.x += self.xv
        self.y += self.yv

    def neighbours(self):
        for d in self.deltas:
            x, y = d
            yield (self.x + x, self.y + y)

    def num_direct_neighbours(self, state):
        cnt = 0
        for n in self.neighbours():
            try:
                assert n in state
                cnt += 1
            except AssertionError:
                pass
        return cnt

    def __repr__(self):
        return "<x: {} y: {} xv: {} yv: {}>".format(self.x, self.y, self.xv, self.yv)


def show(lights, coords):
    result = ""
    minx, miny = min(lights, key=lambda l: l.x).x, min(lights, key=lambda l: l.y).y
    maxx, maxy = max(lights, key=lambda l: l.x).x, max(lights, key=lambda l: l.y).y
    for row in range(miny - 5, maxy + 5):
        result += '\n'
        for col in range(minx - 5, maxx + 5):
            try:
                assert (col, row) in coords
                result += "#"
            except AssertionError:
                result += "."
    print(result)
    time.sleep(5)


if __name__ == '__main__':
    iteration = 0
    # This is a trade off between performance and accuracy but the answer
    # was found with this configuration
    sample_size = 20
    meaningful_threshold = 0.02
    lights = []
    coords = set()
    for line in open('input10').read().splitlines():
        x, y, xv, yv = map(int, re.sub(r"[a-z<>=,]", "", line).split())
        lights.append(Light(x, y, xv, yv))
        coords.add((x, y))

    while True:
        num_aligned = 0.0
        random.shuffle(lights)
        for light in lights[:sample_size]:
            try:
                assert light.num_direct_neighbours(coords) > 1
                num_aligned += 1
            except AssertionError:
                break
        if num_aligned / sample_size >= meaningful_threshold:
            show(lights, coords)
            break
        for l in lights:
            l.tick()
        coords = {(l.x, l.y) for l in lights}
