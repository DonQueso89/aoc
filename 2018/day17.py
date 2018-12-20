import re
import sys
from itertools import chain


rgx = re.compile(r'([xy]{1})=(\d+,\d+)$')


if __name__ == '__main__':
    clay = []
    for line in open(sys.argv[1]):
        line = rgx.sub(r'\1=range(\2 + 1)', line.replace("..", ","))
        exec("clay.append(dict({}))".format(line))

        flattened_clay = set()

    for c in clay:
        try:
            x = list(c['x'])
            y = c['y']
            for sx in x:
                flattened_clay.add((sx, y))
        except TypeError:
            y = list(c['y'])
            x = c['x']
            for sy in y:
                flattened_clay.add((x, sy))

    x_key = lambda k: k[0]
    y_key = lambda k: k[1]
    min_x, max_x = min(flattened_clay, key=x_key)[0], max(flattened_clay, key=x_key)[0]
    min_y, max_y = 0, max(flattened_clay, key=y_key)[1]
    
    display = ""
    for y in range(min_y, max_y + 5):
        display += '\n'
        for x in range(min_x, max_x + 5):
            if (x, y) in flattened_clay:
                display += '#'
            else:
                display += '.'
    print(display)
    print(len(flattened_clay))
