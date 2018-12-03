import re
from collections import defaultdict
data = open('input3').read().splitlines()
state = defaultdict(int)
rgx = re.compile(r"^#(\d+) @ (\d+),(\d+): (\d+)x(\d+)$")
result = 0
no_overlap = None
# left offset, top offset, w, h
for claim in data:
    _id, x, y, w, h = map(int, rgx.match(claim).groups())
    for i in range(x, x + w):
        for j in range(y, y + h):
            state[(i, j)] += 1

for claim in data:
    _id, x, y, w, h = map(int, rgx.match(claim).groups())
    overlaps = False
    for i in range(x, x + w):
        for j in range(y, y + h):
            if state[(i, j)] > 1:
                overlaps = True
                continue
    if overlaps is False:
        no_overlap = _id


print("Part 1: " + str(len([z for z in state.values() if z > 1])))
print("Part 2: " + str(no_overlap))
