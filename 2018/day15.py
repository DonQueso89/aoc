import sys


class Elf(object):
    enemy_unit = 'G'

    def __init__(self, x, y, grid):
        self.hp = 200
        self.x = x
        self.y = y
        self.grid = grid

    def adjacent_open(self):
        """
        Unoccupied adjacent squares
        """
        return [c for c in [
            (self.x - 1, self.y),
            (self.x + 1, self.y),
            (self.x, self.y + 1),
            (self.x, self.y - 1)
        ] if self.grid.get(c) == '.']

    def adjacent_enemies(self):
        """
        Adjacent enemies sorted by (hitpoints, readingorder)
        """
        enemies = [c for c in [
            (self.x - 1, self.y),
            (self.x + 1, self.y),
            (self.x, self.y + 1),
            (self.x, self.y - 1)
        ] if self.grid.get(c) == self.enemy_unit]

        return sorted(enemies, lambda e: (e.hp, e.y, e.x))


class Goblin(Elf):
    enemy_unit = 'E'


if __name__ == '__main__':
    data = open(sys.argv[1]).read().splitlines()
    battlefield = {}

    for y, row in range(len(data)):
        for x, col in enumerate(row):

            battlefield[(x, y)] = col
