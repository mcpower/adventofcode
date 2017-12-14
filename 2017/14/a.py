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

def knot(inp:str):
    n = 256
    lengths = lmap(ord, inp)
    lengths += [17, 31, 73, 47, 23]

    assert isinstance(inp, str)


    pos = 0
    skip = 0

    l = list(range(n))

    for _ in range(64):
        for i in lengths:
            # print(l)
            # l[pos:pos+i] = l[pos:pos+i][::-1]
            positions = [x % n for x in range(pos, pos+i)]
            newpos = positions[::-1]
            # print(positions,newpos)
            newl = list(l)
            for x, y in zip(positions, newpos):
                # print(x,y)
                newl[x] = l[y]
            # print(newl)
            l = newl
            pos += i + skip
            skip += 1

    sparse = []
    for i in range(0, 256, 16):
        from functools import reduce
        sparse.append(reduce(lambda a, b: a ^ b, l[i:i+16]))

    #     q = bin(sparse[-1])[2:].zfill(8)
    #     print(q)
    # print(len(sparse))
    # quit()
    o = "".join(bin(i)[2:].zfill(8) for i in sparse)
    return o

def do_case(inp: str, sample=False):
    l = []
    for i in range(128):
        # print(len(knot(inp + "-" + str(i))))
        l.append([x == '1' for x in knot(inp + "-" + str(i))])
        # print(l[-1])
        assert(len(l[-1]) == 128)
    # o = sum(x == '1' for x in "".join(l))
    # print(o)

    # dfs

    done = [[False] * 128 for _ in range(128)]
    def dfs(x, y):
        if not ( 0 <= x < 128 and 0 <= y < 128):
            return
        if not l[x][y]:
            return
        if done[x][y]:
            return
        done[x][y] = True
        dfs(x+1, y)
        dfs(x-1, y)
        dfs(x, y+1)
        dfs(x, y-1)
        # for dx in [-1, 0, 1]:
        #     for dy in [-1, 0, 1]:
        #         dfs(x + dx, y + dy)
    
    o = 0
    for x in range(128):
        for y in range(128):
            if l[x][y] and not done[x][y]:
                o += 1
                dfs(x, y)
    print(o)

    # r =
    return


samples = [
r"""
flqrgnkx
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
    print("running actual:")
    print("-"*10)
    do_case(actual_input, False)
    print("-"*10)
