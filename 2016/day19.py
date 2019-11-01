import argparse


parser = argparse.ArgumentParser()
parser.add_argument("num_elfs", type=int)


class Elf:
    def __init__(self, n, left=None, right=None, across=None):
        self.n = n
        self.left = left
        self.right = right
        self.num_presents = 1
        self.across = across

    def leave_if_needed(self, num_elves=0):
        if self.num_presents == 0:
            self.left.right = self.right
            self.right.left = self.left
            if num_elves % 2 == 0:
                self.across.across = self.right
            else:
                self.across.across = self.left
            num_elves -= 1
        return num_elves

    def __str__(self):
        return "< |{:d}|{:d}|{:d}| {:d} >".format(
            self.left.n,
            self.n,
            self.right.n,
            self.num_presents
        )


def prep_data(num_elfs):
    first_elf = Elf(1)
    prev_elf = first_elf

    elves = {}
    elves[1] = first_elf
    for i in range(2, num_elfs + 1):
        curr_elf = Elf(i, right=prev_elf)
        prev_elf.left = curr_elf
        prev_elf = curr_elf
        elves[i] = curr_elf
    prev_elf.left = first_elf
    first_elf.right = prev_elf

    for n, elf in elves.items():
        elf.across = elves[across_from_me(elf, num_elfs)]
    return first_elf


def across_from_me(elf, num_elfs):
    if num_elfs % 2 == 0:
        # even: distance is function of circle-size
        across = ((elf.n + num_elfs // 2) % num_elfs) or num_elfs
    else:
        # TODO: uneven: distance is function of circle-size and position
        pass
    return across


def solve(first_elf):
    curr_elf = first_elf
    while True:
        if curr_elf.n == curr_elf.right.n:
            return curr_elf.n

        curr_elf.num_presents += curr_elf.left.num_presents
        curr_elf.left.num_presents = 0
        curr_elf.left.leave_if_needed()
        curr_elf = curr_elf.left


def solve2(first_elf, num_elves):
    curr_elf = first_elf
    while True:
        if curr_elf.n == curr_elf.right.n:
            return curr_elf.n

        curr_elf.num_presents += curr_elf.across.num_presents
        curr_elf.across.num_presents = 0
        num_elves = curr_elf.left.leave_if_needed(num_elves)
        curr_elf = curr_elf.left


if __name__ == '__main__':
    args = parser.parse_args()
    first_elf = prep_data(args.num_elfs)
    #print('Part 1: {:d}'.format(solve(first_elf)))
    print('Part 2: {:d}'.format(solve(first_elf, args.num_elfs)))
