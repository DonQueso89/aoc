from itertools import *

# For Day 1, the sum of the subsets must be sum(all_packages) / 3 (516)
# For Day 2, the sum of the subsets must be sum(all_packages) / 4 (387)

weight_of_subset = 387

# all_packages is the set.
# Function for finding the powerset of all_packages.
# Powerset only returns subsets of len > 4 and len < 7 because  other subsets need no consideration.
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(4, 7))

# Extract packages from file
all_packages = []
fptr = open("input24.txt")
for line in fptr:
    all_packages.append(int(line.strip()))

print "All packages", all_packages

# for each subset s. sum(s) must be equal to sum(set)/3 or sum(set)/4.
# Find all subsets that meet this requirement.
ps = powerset(all_packages)
subsets = []
for subset in ps:
    if sum(subset) == weight_of_subset:
        subsets.append(subset)

# Find all combinations of subsets whose union is equal to the set.
minimum_length = min(map(len, subsets))
products = []
for subset in subsets:
    if len(subset) == minimum_length:
        products.append(reduce(lambda x, y: x * y, subset))

print "Minimum product", min(products)


