#!/usr/bin/env python
import re


def solve(s, e):
    """
    So brute force it hurts
    """
    patt = re.compile("|".join([x * 2 for x in '0123456789']))

    def check(n):
        n = str(n)
        return eval("<=".join(n)) & bool(re.findall(patt, n))

    return sum([check(x) for x in range(s, e)])


def solve2(s, e):
    """
    So brute force it hurts
    """
    patt = ''
    for i in '0123456789':
        patt += '|'.join([
            f'[^{i}]+{i}{i}[^{i}]+',
            f'^{i}{i}[^{i}]+',
            f'[^{i}]+{i}{i}$',
        ])
        patt += '|'
    patt = re.compile(patt[:-1])

    def check(n):
        n = str(n)
        return eval("<=".join(n)) & bool(re.findall(patt, n))

    return sum([check(x) for x in range(s, e)])


if __name__ == '__main__':
    print("Part 1: {:d}".format(solve(248345, 746315)))
    print("Part 2: {:d}".format(solve2(248345, 746315)))
