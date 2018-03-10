import copy
import itertools

# Process input. Grid becomes a list of lists.
fptr = open("input18.txt")
grid = []
for line in fptr:
    grid.append(list(line.rstrip())) 

# Day 2: Configure initial state so that all corner lights are on.
corners = [(0, 0), (0, 99), (99, 0), (99, 99)]
for c in corners:
    grid[c[0]][c[1]] = '#'

print 'Initial state: '
for y in grid:
    print ''.join(y)
print '\n'


# Function for mapping to grid. Takes a list of lists of strings and a tuple representing the coordinates of 
# 1 light and the ones surrounding it. Also takes the list to modify.
# Returns the modified list after 1 modification.
# Indexes go from [0][0] to [99][99]. The first represents y, the second x.
"""
Neighbours in the middle:

([y-1][x-1])([y-1][x])([y-1][x+1])
 ([y][x-1])  ([y][x])  ([y][x+1])
([y+1][x-1]) ([y+1][x]) ([y+1][x+1])

Side = all containing 0 or 99.

"""
steps = 10000
grid_y = 100
grid_x = 100


# Modifies the current state of the grid
def mod(current_state, yx, l):
    # Omit corners for Day 2
    if yx in corners:
        return None
    y = yx[0]
    x = yx[1]
    coordinates = [(y-1, x-1), (y-1, x), (y-1, x+1), (y, x-1), (y, x+1), (y+1, x-1), (y+1, x), (y+1, x+1)]
    # light on the side, reduce coordinates if necessary.
    coordinates = [c for c in coordinates if all(i >= 0 and i <= 99 for i in c)]
    # check surrounding lights.
    count = 0
    for t in coordinates:
        if current_state[t[0]][t[1]] == '#':
            count += 1
    # light is on.
    if current_state[y][x] == '#':
        if count == 2 or count == 3:
            pass
        else:
            l[y][x] = '.'
    # light is off.
    elif current_state[y][x] == '.' and count == 3:
        l[y][x] = '#'

# Takes the grid and modifies all the lights. Returns the grid.
def step(l):
    current_state = copy.deepcopy(l)
    # One cycle through current_state is one step. l is the list to modify.
    for y in range(grid_y):
        for x in range(grid_x):
            mod(current_state, (y, x), l)

# No return statements needed in functions because pointers are passed into them.
# Order: grid --> step --> mod. The functions just modify the list to which the pointers point.
for i in range(steps):
    step(grid)
    for y in grid:
        print ''.join(y)

# Output Day 1 and Day 2.
print 'State after %i steps: ' % steps
c = 0
for y in grid:
    for x in y:
        if x == '#':
            c += 1
    print ''.join(y)
print '\n'
print 'Amount of lights lit: %i' % c
 




