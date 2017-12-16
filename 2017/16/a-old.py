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


def do_case(inp: str, sample=False):
    if sample:
        n = 5
    else:
        n = 16
    l = [chr(ord('a') + i) for i in range(n)]
    for s in inp.split(","):
        op = s[0]
        rest = s[1:]
        newl = list(l)
        if op == "s":
            r  = int(rest)
            newl = l[n-r:] + l[:n-r]
        else:
            if op == 'x':
                x, y = map(int, rest.split("/"))
                newl[x], newl[y] = newl[y], newl[x]
            else:
                x, y = rest.split("/")
                x, y = l.index(x), l.index(y)
                newl[x], newl[y] = newl[y], newl[x]
        l = newl
        if sample: print(l)
    print("".join(l))
    return


samples = [
r"""
s1,x3/4,pe/b
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
