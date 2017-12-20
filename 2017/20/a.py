#!/usr/bin/pypy3
from pprint import pprint
from functools import reduce
import operator
import sys
sys.setrecursionlimit(100000)
lmap = lambda func, *iterables: list(map(func, *iterables))
splitf = lambda s, f=int: lmap(f,s.split())
def d(*a, **k):
    if DEBUG:
        print(*a, **k)

def dd(object):
    if DEBUG:
        pprint(object, compact=True)


DEBUG = 1

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

GRID_DELTA = [[-1, 0], [1, 0], [0, -1], [0, 1]]
OCT_DELTA = [[1, 1], [-1, -1], [1, -1], [-1, 1]] + GRID_DELTA

# unpack your points!!
from collections import Counter
def do_case(inp: str, sample=False):
    sprint = lambda *a, **k: sample and print(*a, **k)
    
    lines = inp.splitlines()

    points = [] # p, v, a
    for line in lines:
        p, v, a = [list(map(int, x[3:].strip("< >").split(",")))for x in line.split(", ")]
        sprint(p, v, a)
        points.append([p, v, a])
    
    def rem(points):
        seen = Counter(tuple(p) for p, v, a in points)
        o = []
        for p, v, a in points:
            pp = tuple(p)
            assert seen[pp]
            if seen[pp] == 1:
                o.append([p, v, a])
        return o

    def update(points):
        
        o = []
        for p, v, a in points:
            v = padd(v, a)
            p = padd(p, v)
            o.append([p, v, a])
        
            
        return o

    for _ in range(10000):
        points = rem(points)
        points = update(points)
    
    
    print(len(points))

    return



samples = [
r"""
p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>
p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>
p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>
p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>
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
