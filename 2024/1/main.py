#!/usr/bin/env python

import argparse
from io import TextIOWrapper
from pathlib import Path

parser = argparse.ArgumentParser(description='day X')

parser.add_argument('input', type=str, help='input file')

dir_ = Path(__file__).parent

def main(infp: TextIOWrapper, args: argparse.Namespace):
    inp = infp.read().splitlines()
    list1, list2 = [], []
    for line in inp:
        number1, number2 = int(line.split()[0]), int(line.split()[-1])
        list1.append(number1)
        list2.append(number2)
    list1.sort()
    list2.sort()


    similarity = 0
    rolling_distance = 0
    for popo,jorso in zip(list1,list2):
        distance = abs(popo-jorso)
        rolling_distance += distance
        similarity += jorso * list1.count(jorso)
    
    print(similarity)





if __name__ == '__main__':
    args = parser.parse_args()
    infp = open(dir_ / args.input.split("/")[-1], 'r')
    main(infp, args)
