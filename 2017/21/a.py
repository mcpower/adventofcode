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

    cur = """.#./..#/###"""

    book = {}

    def to_grid(s):
        return list(map(list, s.split("/")))
    
    # rot 90 deg
    def rot(grid):
        n = len(grid)
        o = [[None]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                o[i][j] = grid[~j][i]
        return o

    def flip(grid):
        return list(map(reversed, grid))
    
    def to_str(s):
        return "/".join("".join(x) for x in s)


    for line in lines:
        a, b = line.split(" => ")

        for rots in range(4):
            for flips in range(2):
                transformed = to_grid(a)
                for _ in range(rots):
                    transformed = rot(transformed)
                for _ in range(flips):
                    transformed = flip(transformed)
                book[to_str(transformed)] = b

    def iteration(grid):
        n = len(grid)
        if n % 2 == 0:
            new_n = n // 2 * 3
            split = 2
            newsplit = 3
        else:
            new_n = n//3 * 4
            split = 3
            newsplit = 4
        

        out = [[None]*new_n for _ in range(new_n)]
        for i in range(0, n // split):
            for j in range(0, n // split):
                si = i * split
                sj = j * split
                g = [row[sj:sj+split] for row in grid[si:si+split]]
                s = to_str(g)
                assert(s in book)
                transf = to_grid(book[s])

                ei = i * newsplit
                ej = j * newsplit
                for a in range(newsplit):
                    for b in range(newsplit):
                        out[ei+a][ej+b] = transf[a][b]
                        
        sprint(out)
        return out

    cur = to_grid(cur)

    for _ in range(18 if not sample else 2):
        cur = iteration(cur)
    
    print(to_str(cur).count("#"))

    # start = 

    return



samples = [
r"""
../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#
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
