#!/usr/bin/pypy3
from pprint import pprint
from functools import reduce
import operator
import sys
from collections import Counter, defaultdict, deque
import math
sys.setrecursionlimit(100000)
lmap = lambda func, *iterables: list(map(func, *iterables))
splitf = lambda s, f=int: lmap(f,s.split())

def knot(inp: str, binary=False) -> str:
    lengths = lmap(ord, inp) + [17, 31, 73, 47, 23]
    pos = skip = 0
    l = list(range(256))
    for _ in range(64):
        for i in lengths:
            positions = [x & 255 for x in range(pos, pos+i)]
            oldl = list(l)
            for x, y in zip(positions, reversed(positions)):
                l[x] = oldl[y]
            pos += i + skip
            skip += 1
    sparse = [reduce(operator.xor, l[i:i+16]) for i in range(0, 256, 16)]
    if binary:
        return "".join(bin(i)[2:].zfill(8) for i in sparse)
    else:
        return "".join(hex(i)[2:].zfill(2) for i in sparse)

padd = lambda x, y: [a+b for a, b in zip(x, y)]
pneg = lambda v: [-i for i in v]
psub = lambda x, y: [a-b for a, b in zip(x, y)]
pmul = lambda m, v: [m * i for i in v]
pdot = lambda x, y: sum(zip(x, y))
pnorm1 = lambda v: sum(map(abs, v))
pnorm2sq = lambda v: sum(i*i for i in v)
pnorm2 = lambda v: math.sqrt(pnorm2sq(v))
pnorminf = lambda v: max(map(abs, v))

GRID_DELTA = [[-1, 0], [1, 0], [0, -1], [0, 1]]
OCT_DELTA = [[1, 1], [-1, -1], [1, -1], [-1, 1]] + GRID_DELTA


def do_case(inp: str, sample=False):
    sprint = lambda *a, **k: sample and print(*a, **k)
    
    lines = inp.splitlines()
    comp = []
    for line in lines:
        comp.append(sorted(map(int, line.split("/"))))
    comp.sort()
    
    d = defaultdict(list)
    for a, b in comp:
        # print(a, b)
        d[a].append(b)
        if a != b:
            d[b].append(a)
    sprint(d)
    
    # assert(len(comp) == len(set(map(tuple, comp))))

    # find max thing cycle
    # find ALL cycles?

    def doit(i, seen):
        o = 0
        chosen = None
        for x in d[i]:
            q = tuple(sorted([i, x]))
            if q not in seen:
                n = set(seen)
                n.add(q)
                o = max(o, sum(q) + doit(x, n))
                chosen = x
        sprint(seen, o)
        return o
    
    z = 0
    for i in [0]:
        z = max(z, doit(i, set()))
    print(z)
    return



samples = [
r"""
0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10
""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""
]
samples = lmap(str.strip, samples)
while samples and not samples[-1]:
    samples.pop()

for sample in samples:
    print("running {}:".format(repr(sample)[:100]))
    print("-"*10)
    do_case(sample, True)
    print("-"*10)
    print("#"*10)

try:
    actual_input = open("input.txt").read().strip()
except FileNotFoundError:
    actual_input = ""

if actual_input:
    print("!! running actual: !!")
    print("-"*10)
    do_case(actual_input, False)
    print("-"*10)
