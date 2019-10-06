import argparse
from itertools import cycle
from functools import partial

parser = argparse.ArgumentParser(description='Solve day 15')
parser.add_argument("infile", type=str)


class Cart:
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def __init__(self, x, y, direction):
        self.direction = direction
        self.x = x
        self.y = y
        self.next_direction = cycle([-1, 0, 1])

    def turn(self, node):
        """
        :param: node:: Corner or Intersection
        """
        if node.is_intersection:
            # intersection
            self.direction = (self.direction + next(self.next_direction)) % 4
        elif node.is_corner:
            if node.is_top_left and self.direction == Cart.WEST:
                self.direction = Cart.SOUTH
            elif node.is_top_left and self.direction == Cart.NORTH:
                self.direction = Cart.EAST
            elif node.is_top_right and self.direction == Cart.NORTH:
                self.direction = Cart.WEST
            elif node.is_top_right and self.direction == Cart.EAST:
                self.direction = Cart.SOUTH
            elif node.is_bottom_right and self.direction == Cart.EAST:
                self.direction = Cart.NORTH
            elif node.is_bottom_right and self.direction == Cart.SOUTH:
                self.direction = Cart.WEST
            elif node.is_bottom_left and self.direction == Cart.SOUTH:
                self.direction = Cart.EAST
            elif node.is_bottom_left and self.direction == Cart.WEST:
                self.direction = Cart.NORTH
            else:
                raise Exception("Cant aproach this corner from this direction")
        else:
            raise ValueError("Corner or Intersection required for turning")

    def go(self, node):
        """
        :param: node:: Node: current node

        return:: Node: next node
        """
        if self.direction == Cart.WEST:
            self.x -= 1
            node.west.carts.append(node.carts.pop())
            return node.west
        if self.direction == Cart.EAST:
            self.x += 1
            node.east.carts.append(node.carts.pop())
            return node.east
        if self.direction == Cart.NORTH:
            self.y -= 1
            node.north.carts.append(node.carts.pop())
            return node.north
        if self.direction == Cart.SOUTH:
            self.y += 1
            node.south.carts.append(node.carts.pop())
            return node.south


class Node:
    is_intersection = False
    is_corner = False
    is_road = False

    def __init__(self, x, y, token, north=None, east=None, west=None, south=None):
        self.x = x
        self.y = y
        self.token = token
        self.north = north
        self.east = east
        self.west = west
        self.south = south
        self.carts = []

    @property
    def collision(self):
        return len(self.carts) > 1


class Road(Node):
    is_road = True

    def __init__(self, *args, **kwargs):
        initial_cart = kwargs.pop('cart', None)
        super().__init__(*args, **kwargs)
        self.is_horizontal = self.east and self.west
        self.is_vertical = self.north and self.south
        if initial_cart:
            self.carts.append(initial_cart)


class Intersection(Node):
    is_intersection = True


class Corner(Node):
    is_corner = True

    def initialize(self):
        self.is_top_right = self.south and self.west
        self.is_top_left = self.east and self.south
        self.is_bottom_left = self.east and self.north
        self.is_bottom_right = self.west and self.north


def graph_from_file(fname):
    grid = {}
    _input = open(fname).read().splitlines()

    # Build the grid
    for y, line in enumerate(_input):
        line = line.strip()
        for x, token in enumerate(line):
            if token == ' ':
                pass
            elif token == '-':
                grid[(x, y)] = Road(x, y, token)
            elif token == '|':
                grid[(x, y)] = Road(x, y, token)
            elif token == '+':
                grid[(x, y)] = Intersection(x, y, token)
            elif token in '/\\':
                grid[(x, y)] = Corner(x, y, token)
            elif token == '<':
                grid[(x, y)] = Road(x, y, '-', cart=Cart(x, y, Cart.WEST))
            elif token == '>':
                grid[(x, y)] = Road(x, y, '-', cart=Cart(x, y, Cart.EAST))
            elif token == '^':
                grid[(x, y)] = Road(x, y, '|', cart=Cart(x, y, Cart.NORTH))
            elif token == 'v':
                grid[(x, y)] = Road(x, y, '|', cart=Cart(x, y, Cart.SOUTH))
            else:
                raise ValueError('Unknown input token ' + token)

    # Connect Nodes
    graph = []
    for (x, y), node in grid.items():
        if node.is_road and node.token == '-':
            node.west, node.east = grid[(x-1, y)], grid[(x + 1, y)]
        elif node.is_road and node.token == '|':
            node.south, node.north = grid[(x, y+1)], grid[(x, y-1)]
        elif node.is_corner and node.token == '/':
            east, south = grid.get((x + 1, y)), grid.get((x, y + 1))
            west, north = grid.get((x - 1, y)), grid.get((x, y - 1))
            if east and east.token in '+-/\\' and south and south.token in '/+|\\':
                node.south = south
                node.east = east
            elif west and west.token in '/\\+-' and north and north.token in '/\\+|':
                node.west = west
                node.north = north
            else:
                import ipdb; ipdb.set_trace()
                raise Exception('hit impossible corner case')
            node.initialize()
        elif node.is_corner and node.token == '\\':
            east, south = grid.get((x + 1, y)), grid.get((x, y + 1))
            west, north = grid.get((x - 1, y)), grid.get((x, y - 1))
            if east and east.token in '/\\+-' and north and north.token in '/\\+|':
                node.north = north
                node.east = east
            elif west and west.token in '/\\+-' and south and south.token in '/\\+|':
                node.west = west
                node.south = south
            else:
                raise Exception('hit impossible corner case')
            node.initialize()
        elif node.is_intersection:
            east, south = grid.get((x + 1, y)), grid.get((x, y + 1))
            west, north = grid.get((x - 1, y)), grid.get((x, y - 1))
            node.east = east
            node.west = west
            node.north = north
            node.south = south
        else:
            raise ValueError("Unsupported NodeType in graph")

        graph.append(node)

    return graph


def solve(graph):
    """
    :param: graph:: Node

    return: (x, y): of last cart
    """
    while True:
        graph = sorted(graph, key=lambda node: (node.y, node.x))
        for node in graph:
            if node.carts:
                cart = node.carts[0]
                next_node = cart.go(node)
                if next_node.is_corner or next_node.is_intersection:
                    cart.turn(next_node)
                if next_node.collision:
                    return (next_node.x, next_node.y)


if __name__ == '__main__':
    args = parser.parse_args()
    graph = graph_from_file(args.infile)
    first_crash = solve(graph)
    print(first_crash)
