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
        self.direction = self.direction_resolver[self.direction][road](self.direction) % 4
        self.x, self.y = self.next_position[self.direction](self.x, self.y)

    def __repr__(self):
        return "[ direction:{} x:{} y:{} ]".format(
            self.nesw[self.direction],
            self.x,
            self.y
        )


class Collision(Exception):
    pass


class CartsByPosition(dict):
    """
    Keep track of carts by position.
    If multiple carts are assigned to the same key, flag a collision.
    """
    def __init__(self, *args, **kwargs):
        carts = kwargs.pop('carts')
        super().__init__(self, *args, **kwargs)
        for cart in carts:
            self[(cart.x, cart.y)] = cart

    def __setitem__(self, k, v):
        """
            If a collision happens, clean out the cart and dont assign it.
        """
        if k in self:
            self.pop(k)
            raise Collision
        super().__setitem__(k, v)


def solve(carts):
    collisions = []
    while True:
        for x, y in sorted(carts, key=lambda k: (k[1], k[0])):
            cart = carts.pop((x, y), None)
            # Cart may have been removed since start of tick
            if cart:
                cart.tick()
                try:
                    carts[(cart.x, cart.y)] = cart
                except Collision:
                    collisions.append((cart.x, cart.y))
            if len(carts) == 1:
                return collisions[0], [x for x in carts.keys()][0]


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
    carts = CartsByPosition(carts=carts)
    first_collision, last_cart_pos = solve(carts)

    print("Part 1: " + str(first_collision))
    print("Part 2: " + str(last_cart_pos))
