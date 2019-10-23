import argparse
import re
import string
from hashlib import md5

parser = argparse.ArgumentParser()
parser.add_argument("salt", type=str)
parser.add_argument("hash_rounds", type=int)


MEMOIZED = {}


def solve(salt, num_hash_rounds=1):
    key_count = 0
    key_tracker = set([])
    three = re.compile(r'{3}|'.join(string.hexdigits[:-6]) + '{3}')
    five = re.compile(r'{5}|'.join(string.hexdigits[:-6]) + '{5}')

    i = 0
    cache_hits = 0
    while True:
        # Purge old keys
        key_tracker -= set([x for x in key_tracker if (i - x[1]) > 1000])

        # Consider new keys
        _hash = md5((salt + str(i)).encode()).hexdigest()
        for _ in range(num_hash_rounds):
            _h = _hash
            if _hash in MEMOIZED:
                cache_hits += 1
            _hash = MEMOIZED.get(_hash) or md5(_hash.encode()).hexdigest()
            MEMOIZED[_h] = _hash

        # Consider solved keys
        keysolvers = set([x[0] for x in five.findall(_hash)])
        resolved = set([])
        for (char, idx) in sorted(key_tracker, key=lambda x: x[1]):
            if char in keysolvers:
                key_count += 1
                if key_count == 64:
                    return idx
                resolved.add((char, idx))
        key_tracker -= resolved
        m = three.search(_hash)
        if m is not None:
            key_tracker.add((_hash[m.span()[0]], i))

        i += 1


if __name__ == '__main__':
    args = parser.parse_args()
    print("Part 1: {:d}".format(solve(args.salt, args.hash_rounds)))
