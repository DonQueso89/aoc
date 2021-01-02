#!/usr/bin/env python
from uuid import uuid4

from lark import Lark

raw_grammar = open("grammar").read()
messages = list(map(lambda x: x.strip(), open("messages").readlines()))

for i in range(129, -1, -1):
    if i == 0:
        raw_grammar = raw_grammar.replace(str(i), "zero")
    else:
        s = ""
        i = str(i)
        for exp, n in enumerate(reversed(i)):
            s = {
                0: {
                    0: "zero",
                    1: "one",
                    2: "two",
                    3: "three",
                    4: "four",
                    5: "five",
                    6: "six",
                    7: "seven",
                    8: "eight",
                    9: "nine",
                },
                1: {
                    0: "",
                    1: "ten",
                    2: "twenty",
                    3: "thirty",
                    4: "forty",
                    5: "fifty",
                    6: "sixty",
                    7: "seventy",
                    8: "eighty",
                    9: "ninety",
                },
                2: {
                    0: "",
                    1: "hundred"
                }
            }[int(exp)][int(n)] + s
        raw_grammar = raw_grammar.replace(i, s)

raw_grammar = raw_grammar.replace(":", " :")
parser = Lark(raw_grammar, start="zero")

n_valid = 0
for msg in messages:
    try:
        parser.parse(msg)
        n_valid += 1
    except Exception:
        pass

print(f"1: {n_valid}")

raw_grammar = raw_grammar.replace("eight : fortytwo\n", "eight : fortytwo | fortytwo eight\n")
raw_grammar = raw_grammar.replace("tenone : fortytwo thirtyone", "tenone : fortytwo thirtyone | fortytwo tenone thirtyone")
parser = Lark(raw_grammar, start="zero")
n_valid = 0
for msg in messages:
    try:
        parser.parse(msg)
        n_valid += 1
    except Exception:
        pass

print(f"2: {n_valid}")
