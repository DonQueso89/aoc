import multiprocessing
import time
import string
data = open('input5').read()


def react(polymer):
    new_polymer = ''
    skip = False
    for i in range(len(polymer)):
        if skip is True:
            skip = False
            continue
        if i == len(polymer) - 1:
            new_polymer += polymer[i]
        elif abs(ord(polymer[i]) - ord(polymer[i + 1])) == 32:
            skip = True
        else:
            new_polymer += polymer[i]
    return new_polymer


def chain_react(polymer):
    new_polymer = polymer
    while True:
        last_polymer = new_polymer
        new_polymer = react(last_polymer)
        if len(new_polymer) == len(last_polymer):
            break
    return len(new_polymer)

print('Part 1: ' + str(chain_react(data)))

state = multiprocessing.Manager().list()
pids = []


def pf(char, state):
    state.append(chain_react(data.replace(char, '').replace(char.upper(), '')))


for ch in string.ascii_lowercase:
    p = multiprocessing.Process(target=pf, args=(ch, state))
    pids.append(p)
    p.start()

for p in pids:
    p.join()

st = time.time()

print('Part 2: ' + str(min(state)))
print(time.time() - st)
