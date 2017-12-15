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

def knot(inp: str):
    n = 256
    lengths = lmap(ord, inp)
    lengths += [17, 31, 73, 47, 23]
    pos = 0
    skip = 0
    l = list(range(n))
    for _ in range(64):
        for i in lengths:
            positions = [x % n for x in range(pos, pos+i)]
            newpos = positions[::-1]
            newl = list(l)
            for x, y in zip(positions, newpos):
                newl[x] = l[y]
            l = newl
            pos += i + skip
            skip += 1
    sparse = []
    for i in range(0, 256, 16):
        from functools import reduce
        sparse.append(reduce(lambda a, b: a ^ b, l[i:i+16]))
    # two hex
    # 8 bin
    # o = "".join(bin(i)[2:].zfill(8) for i in sparse)
    o = "".join(hex(i)[2:].zfill(2) for i in sparse)
    return o

MOD = 2147483647
#PAIRS = 40 * 1000000
def do_case(inp: str, sample=False):

    PAIRS = 5 * 1000000
    ll = inp.splitlines()
    o = []
    for l in ll:
        o.append(int(l.split()[-1]))
    d(o)
    a, b = 16807, 48271
    ca, cb = o
    out = 0
    for _ in range(PAIRS):

        ca *= a
        ca %= MOD
        while ca % 4:
            ca *= a
            ca %= MOD
        cb *= b
        cb %= MOD
        while cb % 8:
            cb *= b
            cb %= MOD
        if ca & ((1<<16) - 1) == cb & ((1<<16) - 1):
            out += 1
    print(out)

    return


samples = [
r"""
65
8921
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
    print("!! running actual: !!")
    print("-"*10)
    do_case(actual_input, False)
    print("-"*10)
