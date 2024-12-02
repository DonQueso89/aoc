import argparse
from io import TextIOWrapper

parser = argparse.ArgumentParser(description='day 10')

parser.add_argument('input', type=str, help='input file')
parser.add_argument("-s", "--startdir", type=str, default="N", help="starting direction")
parser.add_argument("-e", "--extra_rotation", type=str, default="L")


neighbours = {
    "N": lambda x, y: (x, y - 1),
    "S": lambda x, y: (x, y + 1),
    "E": lambda x, y: (x + 1, y),
    "W": lambda x, y: (x - 1, y),
}

def rotate(left_or_right):
    def _rotate(dir):
        if left_or_right == "L":
            return {
                "N": "W",
                "W": "S",
                "S": "E",
                "E": "N",
            }[dir]
        elif left_or_right == "R":
            return {
                "N": "E",
                "E": "S",
                "S": "W",
                "W": "N",
            }[dir]
        else:
            return dir
    return _rotate

turn = {
    ("E","7"): rotate("R"),
    ("E","J"): rotate("L"),
    ("W","L"): rotate("R"),
    ("W","F"): rotate("L"),
    ("N","7"): rotate("L"),
    ("S","J"): rotate("R"),
    ("N","F"): rotate("R"),
    ("S","L"): rotate("L"),
    ("E","-"): rotate(None),
    ("W","-"): rotate(None),
    ("N","|"): rotate(None),
    ("S","|"): rotate(None),
}

def _next(dir, x, y):
    return {
    "S": (x, y + 1),
    "N": (x, y - 1),
    "E": (x + 1, y),
    "W": (x - 1, y),
    }[dir]

def prettyprint(grid, loop, inside_grid=None):
    green = "\033[92m{}\033[00m"
    red= "\033[91m{}\033[00m"
    yellow= "\033[93m{}\033[00m"
    cyan = "\033[96m{}\033[00m"
    sb_ = ""
    maxx = max(*[x for (x, _) in grid])
    maxy= max(*[y for (_, y) in grid])
    for y in range(maxy + 1):
        for x in range(maxx + 1):
            if grid[(x, y)] == "S":
                sb_ += red.format(grid[(x, y)])
            elif (inside_grid is not None) and ((x, y) in inside_grid):
                sb_ += cyan.format("*")
            elif grid[(x, y)] == ".":
                sb_ += yellow.format(".")
            elif (x, y) in loop:
                sb_ += green.format(grid[(x, y)])
            else:
                sb_ += grid[(x, y)]
        sb_ += "\n"
    print(sb_)

def main(infp: TextIOWrapper, args: argparse.Namespace):
    inp = infp.read().splitlines()

    grid = {}
    loop = {}
    start = None
    for y, line in enumerate(inp):
        for x, c in enumerate(line):
            grid[(x, y)] = c
            if c == "S":
                start = (x, y)

    _orig = start
    dist = 0
    dir_ = args.startdir
    next_ = None
    inside = None
    while next_ != "S":
        loop[start] = dist
        nx, ny = _next(dir_, *start)

        if inside is None and grid[start] == "|" and neighbours["W"](*start) not in grid:
            inside = "E"
        if inside is None and grid[start] == "|" and neighbours["E"](*start) not in grid:
            inside = "W"
        if (nx, ny) not in grid:
            raise ValueError(f"Out of bounds: {nx}, {ny}")

        next_ = grid[(nx, ny)]
        if (rotation := turn.get((dir_, next_))) is not None:
            dir_ = rotation(dir_)
            start = (nx, ny)
            dist += 1
            if inside is not None:
                inside = rotation(inside)
    
    print("part 1")
    print((dist // 2) + 1)


    inside = rotate(args.extra_rotation)(inside)
    inside_grid = set()
    dir_ = args.startdir
    next_ = None
    start = _orig
    while next_ != "S":
        if (_neighbour := neighbours[inside](*start)) not in loop and _neighbour in grid:
            inside_grid.add(_neighbour)

        nx, ny = _next(dir_, *start)
        next_ = grid[(nx, ny)]
        if (rotation := turn.get((dir_, next_))) is not None:
            dir_ = rotation(dir_)
            start = (nx, ny)
            if (_neighbour := neighbours[inside](*start)) not in loop and _neighbour in grid:
                inside_grid.add(_neighbour)
            inside = rotation(inside)

    # floodfill to find all reachable
    stack = list(inside_grid)
    while stack:
        cur = stack.pop()
        for n in neighbours.values():
            candidate = n(*cur)
            if candidate not in loop and candidate not in inside_grid:
                inside_grid.add(candidate)
                stack.append(candidate)

    print("part 2")
    print(len(inside_grid))

if __name__ == '__main__':
    args = parser.parse_args()
    infp = open(args.input, 'r')
    main(infp, args)
