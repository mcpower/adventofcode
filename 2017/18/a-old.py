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


def do_case(inp: str, sample=False):
    sprint = lambda *a, **k: sample and print(*a, **k)
    
    inst = inp.splitlines()

    from collections import defaultdict
    d = defaultdict(int)

    cur = 0

    last = None
    
    i = 0
    while 0 <= cur < len(inst):
        c = inst[cur]
        a, *b = c.split()

        if a == "snd" or a == "rcv":
            other = b[0]
            if a == "snd":
                last = d[other]
            else:
                if d[other] != 0:
                    print(last)
                    return
        else:
            x, y = b
            try:
                y = int(y)
            except Exception:
                y = d[y]
            # if x.isdigit():
            #     x = int(x)
            # if y.is():
            #     y = int(y)
            # else:
            #     y = d[y]
            if a == "set":
                d[x] = y
            if a == "add":
                d[x] += y
            if a == "mul":
                d[x] *= y
            if a == "mod":
                d[x] %= y
            if a == "jgz":
                if d[x] > 0:
                    cur += y
                    cur -= 1
        
        
        cur += 1

        i += 1



    return


samples = [
r"""
set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2
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
