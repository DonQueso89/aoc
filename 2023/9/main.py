import argparse
import functools
from io import TextIOWrapper

parser = argparse.ArgumentParser(description='day 9')

parser.add_argument('input', type=str, help='input file')

def next_value(seq: list[int]) -> int:
    if functools.reduce(lambda x, y: x | y, seq, 0) == 0:
        return seq[-1]
    else:
        derivative = [seq[i+1] - seq[i] for i in range(0, len(seq) -1)]
        return next_value(derivative) + seq[-1]

def prev_value(seq: list[int]) -> int:
    if functools.reduce(lambda x, y: x | y, seq, 0) == 0:
        return seq[0]
    else:
        derivative = [seq[i+1] - seq[i] for i in range(0, len(seq) -1)]
        return seq[0] - prev_value(derivative)

def main(infp: TextIOWrapper):
    seqs = [[int(x.strip()) for x in line.strip().split()] for line in infp.read().splitlines()]
    result = 0
    result2 = 0
    for seq in seqs:
        result += next_value(seq)
        result2 += prev_value(seq)
    print(result) 
    print(result2) 


if __name__ == '__main__':
    args = parser.parse_args()
    infp = open(args.input, 'r')
    main(infp)