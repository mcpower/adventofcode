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
    # print(inp)

    d = defaultdict(int)

    cur_dir = [-1, 0]

    def left(v):
        x, y = v
        return [-y, x]
    
    def right(v):
        x, y = v
        return [y, -x]

    n = len(lines)

    for i in range(n):
        for j in range(n):
            if lines[i][j] == '#':
                d[(i, j)] = 2
    
    cur = [n//2, n//2]
    out = 0
    for _ in range(10000000):
        state = d[tuple(cur)]
        
        if state == 0:
            cur_dir = left(cur_dir)
        elif state == 1:
            # pass
            out += 1
        elif state == 2:
            cur_dir = right(cur_dir)
        else:
            cur_dir = left(left(cur_dir))
            
        
        d[tuple(cur)] += 1
        d[tuple(cur)] %= 4
        cur = padd(cur_dir, cur)

    # print(d)
    print(max(d, key=pnorm1))
    print(out)
    return



samples = [
r"""
..#
#..
...
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
