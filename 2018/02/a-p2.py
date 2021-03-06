from pprint import pprint
from functools import reduce
import functools
import operator
import sys
from collections import Counter, defaultdict, deque
import collections
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


def matmat(a, b):
    n, k1 = len(a), len(a[0])
    k2, m = len(b), len(b[0])
    assert k1 == k2
    out = [[None] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            out[i][j] = sum(a[i][k] * b[k][j] for k in range(k1))
    return out


def matvec(a, v):
    return [j for i in matmat(a, [[x] for x in v]) for j in i]

padd = lambda x, y: [a+b for a, b in zip(x, y)]
pneg = lambda v: [-i for i in v]
psub = lambda x, y: [a-b for a, b in zip(x, y)]
pmul = lambda m, v: [m * i for i in v]
pdot = lambda x, y: sum(a*b for a, b in zip(x, y))
pnorm1 = lambda v: sum(map(abs, v))
pnorm2sq = lambda v: sum(i*i for i in v)
pnorm2 = lambda v: math.sqrt(pnorm2sq(v))
pnorminf = lambda v: max(map(abs, v))

GRID_DELTA = [[-1, 0], [1, 0], [0, -1], [0, 1]]
OCT_DELTA = [[1, 1], [-1, -1], [1, -1], [-1, 1]] + GRID_DELTA



def do_case(inp: str, sample=False):
    sprint = lambda *a, **k: sample and print(*a, **k)
    lines = inp.splitlines()
    twice = 0
    three = 0
    for i in lines:
        for j in lines:
            if i == j: continue
            
            q = [(a,b) for a, b in zip(i, j) if a != b]
            if len(q) == 1:
                print(i,j,q)
    print(twice, three)
    print(twice * three)

    return  # RETURNED VALUE DOESN'T DO ANYTHING, PRINT THINGS INSTEAD



def parse_samples(l):
    samples = lmap(str.strip, l)
    while samples and not samples[-1]:
        samples.pop()
    return samples

# Part 1
samples = parse_samples([
r"""
abcdef
bababc
abbcde
abcccd
aabcdd
abcdee
ababab
""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""
])

# Part 2
samples = parse_samples([
r"""
abcde
fghij
klmno
pqrst
fguij
axcye
wvxyz
""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

""",r"""

"""
]) or samples

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
