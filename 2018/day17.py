import re
import sys
from itertools import chain
import time


rgx = re.compile(r'([xy]{1})=(\d+,\d+)$')


SAND = 0
WATER_AT_REST = 1
MOVING_WATER = 2
CLAY = 3


VISUAL = {
    SAND: '.',
    WATER_AT_REST: '~',
    MOVING_WATER: '|',
    CLAY: '#',
}


LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3


def display(grid, x, y):
    max_x, max_y = x + 50, y + 30
    for _y in range(y - 10, max_y + 1):
        line = ""
        for _x in range(x - 100, max_x):
            if (x, y) == (_x, _y):
                line += ("$")
            else:
                line += (VISUAL[grid.get((_x, _y), SAND)])
        print(line)


HTML = """
<html lang="en">
<head>
  <meta charset="utf-8">

  <title>Grid dump</title>
  <meta name="description" content="Grid dump">
  <meta name="author" content="SitePoint">

</head>

<body>
<pre style='font-family:monospace'>
{}
</pre>
</body>
</html>
"""


def write(grid, x, y):
    max_x, max_y = max(grid, key=lambda k: k[0])[0], max(grid, key=lambda k: k[1])[1]
    blob = ""

    for _y in range(0, max_y + 1):
        line = ""
        for _x in range(0, max_x + 100):
            if (x, y) == (_x, _y):
                line += ("$")
            else:
                line += (VISUAL[grid.get((_x, _y), SAND)])
        line += '\n'

        blob += line

    with open("./grid_dump.html", "w+") as fp:
        fp.write(HTML.format(blob))


def prep_data():
    clay = []
    for line in open(sys.argv[1]):
        line = rgx.sub(r'\1=range(\2 + 1)', line.replace("..", ","))
        exec("clay.append(dict({}))".format(line))

    grid = {}
    min_y = 1 << 64
    for c in clay:
        try:
            x = list(c['x'])
            y = c['y']
            min_y = min(min_y, y)
            for sx in x:
                grid[(sx, y)] = CLAY
        except TypeError:
            y = list(c['y'])
            x = c['x']
            for sy in y:
                min_y = min(min_y, sy)
                grid[(x, sy)] = CLAY
    return grid, min_y


NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3


def solve(grid, min_y):
    """
    set potential_rest_reference to None, Go S
    If I can't go S, append splitpoint to queue and set direction to W
    If I can't go W:
        - set current coordinate as potential_rest_reference
        - pop the last splitpoint and go E
    If I can't go E:
        - mark the potential_rest_reference until this coordinate as water at rest
        - set potential_rest_reference to None
        - set coordinate to 1 above me, go W
    If going S and outofbounds, pop the last splitpoint and go E
    No more splitpoints = game over

    state of current coordinate is function of direction and next_coordinate area
    """
    x, y = 500, 0
    direction = SOUTH
    max_y = max(grid, key=lambda k: k[1])[1]
    splitpoint_queue = []
    potential_bassin_ref = None
    while True:
        dirs = {
            NORTH: lambda _x, _y: (_x, _y - 1),
            SOUTH: lambda _x, _y: (_x, _y + 1),
            WEST: lambda _x, _y: (_x - 1, _y),
            EAST: lambda _x, _y: (_x + 1, _y),
        }
        next_x, next_y = dirs[direction](x, y)

        if next_y > max_y:
            grid[(x, y)] = MOVING_WATER
            if splitpoint_queue:
                x, y = splitpoint_queue.pop()
                direction = EAST
                while grid[(x, y)] == WATER_AT_REST:
                    if splitpoint_queue:
                        x, y = splitpoint_queue.pop()
                    else:
                        write(grid, x, y)
                        return sum([v in (WATER_AT_REST, MOVING_WATER) for k, v in grid.items() if min_y <= k[1] <= max_y]), sum([v in (WATER_AT_REST,) for k, v in grid.items() if min_y <= k[1] <= max_y])

                continue
            else:
                write(grid, x, y)
                return sum([v in (WATER_AT_REST, MOVING_WATER) for k, v in grid.items() if min_y <= k[1] <= max_y]), sum([v in (WATER_AT_REST,) for k, v in grid.items() if min_y <= k[1] <= max_y])


        next_area = grid.get((next_x, next_y), SAND)
        area_below = grid.get(dirs[SOUTH](x, y), SAND)
        if area_below == SAND:
            grid[(x, y)] = MOVING_WATER
            x, y = dirs[SOUTH](x, y)
            direction = SOUTH
            potential_bassin_ref = None
        elif direction == SOUTH and next_area in (CLAY, WATER_AT_REST) and grid.get((x, y), SAND) == MOVING_WATER and grid.get((x - 1, y), SAND) == MOVING_WATER:
            grid[(x, y)] = MOVING_WATER
            if splitpoint_queue:
                x, y = splitpoint_queue.pop()
                direction = EAST
                while grid[(x, y)] == WATER_AT_REST:
                    if splitpoint_queue:
                        x, y = splitpoint_queue.pop()
                    else:
                        write(grid, x, y)
                        return sum([v in (WATER_AT_REST, MOVING_WATER) for k, v in grid.items() if min_y <= k[1] <= max_y]), sum([v in (WATER_AT_REST,) for k, v in grid.items() if min_y <= k[1] <= max_y])

                continue
            else:
                write(grid, x, y)
                return sum([v in (WATER_AT_REST, MOVING_WATER) for k, v in grid.items() if min_y <= k[1] <= max_y]), sum([v in (WATER_AT_REST,) for k, v in grid.items() if min_y <= k[1] <= max_y])

        elif direction == SOUTH and next_area in (CLAY, WATER_AT_REST):
            grid[(x, y)] = MOVING_WATER
            splitpoint_queue.append((x, y))
            direction = WEST
        elif direction == SOUTH and next_area == MOVING_WATER:
            grid[(x, y)] = MOVING_WATER
            x, y = dirs[SOUTH](x, y)
        elif direction in (WEST, EAST) and area_below in (SAND, MOVING_WATER):
            grid[(x, y)] = MOVING_WATER
            direction = SOUTH
            x, y = dirs[SOUTH](x, y)
        elif direction == WEST and next_area in (SAND, MOVING_WATER):
            grid[(x, y)] = MOVING_WATER
            x, y = next_x, next_y
        elif direction == WEST and next_area == CLAY:
            grid[(x, y)] = MOVING_WATER
            potential_bassin_ref = (x, y)
            x, y = splitpoint_queue[-1]
            direction = EAST
        elif direction == EAST and next_area == CLAY and potential_bassin_ref is None:
            """
            ...|.......
            ...|......
            |||||||###
            |#########
            |#########
            |#########
            """
            grid[(x, y)] = MOVING_WATER
            if splitpoint_queue:
                x, y = splitpoint_queue.pop()
                while grid[(x, y)] == WATER_AT_REST:
                    if splitpoint_queue:
                        x, y = splitpoint_queue.pop()
                    else:
                        write(grid, x, y)
                        return sum([v in (WATER_AT_REST, MOVING_WATER) for k, v in grid.items() if min_y <= k[1] <= max_y]), sum([v in (WATER_AT_REST,) for k, v in grid.items() if min_y <= k[1] <= max_y])


                continue
            else:
                write(grid, x, y)
                return sum([v in (WATER_AT_REST, MOVING_WATER) for k, v in grid.items() if min_y <= k[1] <= max_y]), sum([v in (WATER_AT_REST,) for k, v in grid.items() if min_y <= k[1] <= max_y])

        elif direction == EAST and next_area in (SAND, MOVING_WATER):
            grid[(x, y)] = MOVING_WATER
            x, y = next_x, next_y
        elif direction == EAST and next_area == CLAY:
            ref_x, _ = potential_bassin_ref
            for _x in range(ref_x, x + 1):
                grid[(_x, y)] = WATER_AT_REST
            potential_bassin_ref = None
            # Go back to where we entered the cup and go up
            x, y = splitpoint_queue.pop()
            x, y = dirs[NORTH](x, y)
            direction = WEST
            splitpoint_queue.append((x, y))
        else:
            raise Exception("Hit unknown case")
        #display(grid, x, y)
        #time.sleep(0.01)


if __name__ == '__main__':
    grid, min_y = prep_data()
    print("Part 1: {:d}\nPart 2: {:d}".format(*solve(grid, min_y)))
