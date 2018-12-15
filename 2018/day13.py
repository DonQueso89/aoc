import sys
from itertools import cycle
from collections import defaultdict


class Cart(object):
    nesw = '^>v<'
    next_position = {
        0: lambda x, y: (x, y - 1),
        1: lambda x, y: (x + 1, y),
        2: lambda x, y: (x, y + 1),
        3: lambda x, y: (x - 1, y)
    }

    def __init__(self, x, y, direction):
        # LSR --> functions to update direction
        self.turn = cycle([
            lambda x: x - 1,
            lambda x: x,
            lambda x: x + 1
        ])
        self.x = x
        self.y = y
        self.direction = self.nesw.index(direction)

        # direction -> road -> turn
        self.direction_resolver = {
            0: {  # N
                '/': lambda x: x + 1,
                '\\': lambda x: x - 1,
                '|': lambda x: x,
                '-': lambda x: x,
                '+': lambda x: next(self.turn)(x)
            },
            3: {  # W
                '/': lambda x: x - 1,
                '\\': lambda x: x + 1,
                '|': lambda x: x,
                '-': lambda x: x,
                '+': lambda x: next(self.turn)(x)
            },
            2: {  # S
                '/': lambda x: x + 1,
                '\\': lambda x: x - 1,
                '|': lambda x: x,
                '-': lambda x: x,
                '+': lambda x: next(self.turn)(x)
            },
            1: {  # E
                '/': lambda x: x - 1,
                '\\': lambda x: x + 1,
                '|': lambda x: x,
                '-': lambda x: x,
                '+': lambda x: next(self.turn)(x)
            }
        }

    def tick(self):
        road = self.grid[(self.x, self.y)]
        d = self.direction_resolver[self.direction][road](
            self.direction
        )
        if d < 0:
            self.direction = 4 - abs(d)
        else:
            self.direction = d % 4
        self.x, self.y = self.next_position[self.direction](self.x, self.y)

    def __repr__(self):
        return "[ direction:{} x:{} y:{} ]".format(
            self.nesw[self.direction],
            self.x,
            self.y
        )


def next_collision_state(carts):
    coords = defaultdict(int)
    for cart in carts:
        cart.tick()
        coords[(cart.x, cart.y)] += 1

    return [k for k, v in coords.items() if v > 1], carts


if __name__ == '__main__':
    data = [x for x in open(sys.argv[1]).read().splitlines()]
    grid = {}
    carts = []
    for y, row in enumerate(data):
        for x, cell in enumerate(row):
            if cell in Cart.nesw:
                carts.append(Cart(x, y, cell))
                if cell in '<>':
                    grid[(x, y)] = '-'
                else:
                    grid[(x, y)] = '|'
            else:
                grid[(x, y)] = cell

    Cart.grid = grid
    collisions = []

    while not collisions:
        collisions, carts = next_collision_state(carts)

    print("Part 1: " + str(collisions[0]))

    carts = [cart for cart in carts if (cart.x, cart.y) not in collisions]

    while len(carts) > 1:
        collisions, carts = next_collision_state(carts)
        if len(collisions) > 0:
            carts = [cart for cart in carts if (cart.x, cart.y) not in collisions]
    print("Part 2: " + str(carts[0]))

