from collections import Counter
from itertools import product
from functools import reduce

data = open('input2').read().splitlines()


def score(a, e):
    c = Counter(e).values()
    x, y = a
    if 2 in c:
        x += 1
    if 3 in c:
        y += 1
    return (x, y)


def distance(a, e):
    x, y = e
    if x != y:
        return a + 1
    return a


def reducer(a, e):
    dist = reduce(distance, zip(*e), 0)
    if dist == 1:
        return e
    return a


x, y = reduce(score, data, (0, 0))
print('Part 1: ' + str(x * y))
combs = product(data, repeat=2)
result = reduce(reducer, combs)
print('Part 2: ' + str(''.join([a for a, b in zip(*result) if a == b])))
