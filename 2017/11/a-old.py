#!/usr/bin/pypy3
from pprint import pprint
from functools import reduce
import operator
lmap = lambda func, *iterables: list(map(func, *iterables))
splitf = lambda s, f=int: lmap(f,s.split())
def d(*a, **k):
    if DEBUG:
        print(*a, **k)

def dd(object):
    if DEBUG:
        pprint(object, compact=True)


DEBUG = 1

def do_case(inp: str, sample=False):
    l = inp.split(",")
    p = [0, 0]
    for x in l:
        if x == "n":
            p[0] += 1
        if x == "ne":
            p[1] += 1
        if x == "se":
            p[0] -= 1
            p[1] += 1
        if x == "s":
            p[0] -= 1
        if x == "sw":
            p[1] -= 1
        if x == "nw":
            p[1] -= 1
            p[0] += 1
    x = p[0]
    z = p[1]
    y = -x-z
    d = max(abs(x), abs(y), abs(z))
    print(d)
    print(p)
    return


samples = [
r"""
ne,ne,ne
""",r"""
ne,ne,sw,sw
""",r"""
ne,ne,s,s
""",r"""
se,sw,se,sw,sw
""",r"""

""",r"""

""",r"""

"""
]
samples = lmap(str.strip, samples)
while samples and not samples[-1]:
    samples.pop()

for sample in samples:
    print(f"running {repr(sample)[:100]}:")
    print("-"*10)
    do_case(sample, True)
    print("-"*10)
    print("#"*10)

try:
    actual_input = open("input.txt").read().strip()
except FileNotFoundError:
    actual_input = ""

if actual_input:
    print("running actual:")
    print("-"*10)
    do_case(actual_input, False)
    print("-"*10)
