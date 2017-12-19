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
    
    sprint(inp)

    grid = inp.splitlines()
    import string

    out = ""
    pos = None
    n = len(grid)
    m = len(grid[0])
    if not pos:
        for i in range(m):
            if grid[0][i] != " ":
                pos = [0, i]
                break
    assert(pos)

    direction = [1, 0]

    def add(x, y):
        return [a+b for a, b in zip(x, y)]
    next_up = add(direction, pos)
    def in_bounds(l):
        if 0 <= l[0] < n and 0 <= l[1] < m:
            return True
        return False

    print("!", pos)
    steps = 1

    while in_bounds(next_up) and grid[next_up[0]][next_up[1]] != " ":
        x, y = next_up
        if grid[x][y] == "+":
            # change dir
            deltas = [[-1, 0], [1, 0], [0, -1], [0, 1]]

            for d in deltas:
                nn = add(next_up, d)
                if nn != pos and in_bounds(nn) and grid[nn[0]][nn[1]] != " ":
                    direction = d
                    break
            else:
                assert False
        
        pos = next_up
        if grid[x][y] in string.ascii_letters:
            out += grid[x][y]
        next_up = add(direction, pos)
        # print(pos)
        steps += 1
    
    print(out)
    print(steps + 1)


samples = [
r"""     |          
     |  +--+    
     A  |  C    
 F---|----E|--+ 
     |  |  |  D 
     +B-+  +--+
               """,
]
# samples = lmap(str.strip, samples)
while samples and not samples[-1]:
    samples.pop()

for sample in samples:
    print("running {}:".format(repr(sample)[:100]))
    print("-"*10)
    do_case(sample, True)
    print("-"*10)
    print("#"*10)

try:
    actual_input = open("input.txt").read()
except FileNotFoundError:
    actual_input = ""

if actual_input:
    print("!! running actual: !!")
    print("-"*10)
    do_case(actual_input, False)
    print("-"*10)
