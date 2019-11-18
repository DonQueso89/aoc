def next_exit_value(r):
    x = 8595037
    x += (r & 255)
    x &= 16777215
    x *= 65899
    x &= 16777215
    while 256 <= r:
        r //= 256
        x += (r & 255)
        x &= 16777215
        x *= 65899
        x &= 16777215
    return x


if __name__ == '__main__':
    n = next_exit_value(65536)
    print("Part 1: {:d}".format(n))
    cache = set([n])
    while True:
        _orig_n = n
        n = next_exit_value(n | 65536)
        if n in cache:
            break
        cache.add(n)
    print("Part 2: {:d}".format(_orig_n))
