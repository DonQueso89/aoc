"""
The pathfinding algorithm is horribly inefficient but it is a first attempt at
such an algorithm
"""
import argparse

parser = argparse.ArgumentParser(description='Solve day 15')
parser.add_argument("infile", type=str)


class Cell:
    is_unit = False
    is_elf = False
    is_goblin = False
    is_wall = False
    is_open = False

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_enemy(self, *args):
        return False

    def adjacent(self):
        """
        In reading order
        """
        for x, y in [
            (self.x, self.y - 1),
            (self.x - 1, self.y),
            (self.x + 1, self.y),
            (self.x, self.y + 1),
        ]:
            yield x, y

    def __repr__(self):
        return "<{} {} {}>".format(
            self.__class__.__name__,
            str(self.x),
            str(self.y)
        )


class Unit(Cell):
    is_unit = True

    def __init__(self, x, y):
        super().__init__(x, y)
        self.hp = 200
        self.ap = 3

    def is_enemy(self, other):
        return (other.is_goblin and self.is_elf) or (self.is_goblin and other.is_elf)

    @property
    def is_dead(self):
        return self.hp <= 0

    def move_to(self, x, y, grid):
        grid[(x, y)] = self
        grid[(self.x, self.y)] = Open(self.x, self.y)
        self.x = x
        self.y = y


class Goblin(Unit):
    is_goblin = True


class Elf(Unit):
    is_elf = True


class Wall(Cell):
    is_wall = True


class Open(Cell):
    is_open = True


def find_paths(origin, target, grid):
    """
    Get all possible paths from origin to target

    :param: origin:: Unit
    :param: target:: Unit
    :param: grid:: dict of shape {(x, y, tx, ty) => Cell()}

    return: is_blocked:: bool, dict of cells adjacent to origin
        {
            (x, y, tx, ty) => distance_from_target
        }
        where:
            - x, y is  the coordinate of the move
            - tx, ty is the coordinate of the target (we need this for the sort-key)
    """
    queue = {(target.x, target.y): 0}
    target_reached = False
    done = False
    while not done:
        new_cells = {}
        for (cx, cy), distance in queue.items():
            for x, y in grid[(cx, cy)].adjacent():
                # we cant be out of bounds
                # cuz there are surrounding walls
                adjacent_cell = grid[(x, y)]
                if adjacent_cell.is_open and queue.get((x, y), 999999) > distance + 1 and new_cells.get((x, y), 999999) > distance + 1:
                    new_cells[(x, y)] = distance + 1
                if adjacent_cell.x == origin.x and adjacent_cell.y == origin.y:
                    target_reached = True

        for k, v in new_cells.items():
            queue[k] = v

        if target_reached:
            return False, {(x, y, target.x, target.y): d for (x, y), d in queue.items() if (x, y) in [z for z in origin.adjacent()]}

        if not new_cells:
            return True, None

    raise Exception("Reached end of pathfinder. There is a path, or it is blocked, never neither.")


def attack_if_possible(player, grid):
    """
    Check if we can attack.
    Attack the player with the fewest hitpoints

    :param: player:: Unit
    :param: grid:: dict[(int, int) => Cell]

    return: the Unit that was attacked or None:: Unit
    """
    adjacent_cells = [grid[(px, py)] for px, py in player.adjacent()]
    eligible_for_attack = [p for p in adjacent_cells if p.is_enemy(player)]
    if eligible_for_attack:
        victim = sorted(eligible_for_attack, key=lambda k: (k.hp, k.y, k.x))[0]
        victim.hp -= 3
        return victim
    return None


def can_move(p, grid):
    adjacent_cells = [grid[(x, y)] for x, y in p.adjacent()]
    return any(p.is_open for p in adjacent_cells)


def funeral(victim, grid, num_goblins, num_elves):
    """
    Bury a victim if necessary

    :param: player:: Unit
    :param: grid:: dict[(int, int) => Cell]

    return: num_goblins_left, num_elves_left
    """
    if victim.is_dead:
        grid[(victim.x, victim.y)] = Open(victim.x, victim.y)
        return num_goblins - int(victim.is_goblin), num_elves - int(victim.is_elf)
    return num_goblins, num_elves


def solve(grid):
    """
    :param: grid:: dict of shape {(x, y) => Cell()}

    return:
        sum_hp_remaining_units, num_rounds
    """
    num_rounds = 0
    num_goblins = len([x for x in grid.values() if x.is_goblin])
    num_elves = len([x for x in grid.values() if x.is_elf])
    while True:
        # sort players in reading order
        turn_order = sorted([(p.x, p.y) for p in grid.values() if p.is_unit], key=lambda k: (k[1], k[0]))
        for x, y in turn_order:
            # player may have died since start of round
            player = grid[(x, y)]
            if not player.is_unit:
                continue

            enemies_in_range = [p for p in grid.values() if p.is_enemy(player)]
            if not enemies_in_range:
                return sum([x.hp for x in grid.values() if x.is_unit]), num_rounds

            # check if we can attack immediately
            victim = attack_if_possible(player, grid)
            if victim:
                num_goblins, num_elves = funeral(victim, grid, num_goblins, num_elves)
                continue

            # Pre-filter enemies
            enemies_in_range = [p for p in enemies_in_range if can_move(p, grid)]

            # determine the optimal move
            possible_moves = {}
            for enemy in enemies_in_range:
                blocked, paths = find_paths(player, enemy, grid)
                if not blocked:
                    for x, y, tx, ty in paths:
                        dist = paths[(x, y, tx, ty)]
                        possible_moves[(x, y, tx, ty)] = dist
            # Sort by distance, then by target coordinate reading order, then by reading order of move coordinate
            if possible_moves:
                x, y, _, _, _ = sorted([(x, y, tx, ty, d) for (x, y, tx, ty), d in possible_moves.items()], key=lambda k: (k[4], k[3], k[2], k[1], k[0]))[0]
                player.move_to(x, y, grid)
            else:
                continue
            # Check if we can attack now
            victim = attack_if_possible(player, grid)
            if victim:
                num_goblins, num_elves = funeral(victim, grid, num_goblins, num_elves)
        num_rounds += 1
        print("ROUND: {} OVER".format(str(num_rounds)))

    raise Exception("Game did not end properly")


def prep_grid(infile):
    grid = {}
    for y, line in enumerate(open(infile).read().splitlines()):
        for x, cell in enumerate(line):
            if cell == '#':
                grid[(x, y)] = Wall(x, y)
            elif cell == '.':
                grid[(x, y)] = Open(x, y)
            elif cell == 'G':
                grid[(x, y)] = Goblin(x, y)
            elif cell == 'E':
                grid[(x, y)] = Elf(x, y)
            else:
                raise TypeError("Unknown inputtype")

    return grid


if __name__ == '__main__':
    args = parser.parse_args()
    grid = prep_grid(args.infile)
    sum_hp_remaining, n_rounds = solve(grid)
    print("Part 1: " + str(sum_hp_remaining * n_rounds), sum_hp_remaining, n_rounds)
