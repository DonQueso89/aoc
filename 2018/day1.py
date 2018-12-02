from itertools import cycle

fp = open('input1').read().splitlines()
total = 0
for x in fp:
    total = eval("total" + x)

print('Part 1: ' + str(total))

seen = set()
t = 0
for x in cycle(fp):
    seen.add(t)
    t = eval("t" + x)
    if t in seen:
        break

print('Part 2: ' + str(t))
